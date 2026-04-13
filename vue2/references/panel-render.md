# 监控面板渲染组件 (`PanelRender`) 规范

## 使用场景
用于将后端配置的图表和指标面板动态渲染到前端。通过传入后端的面板 `uid`，前端可以自动拉取配置并渲染图表。同时也支持利用具名插槽来“劫持”某一个具体的图表区域，用以进行（高度定制化）的前端自定义渲染（结合自定义 ECharts 等组件）。

## 伪代码骨架
该组件通常从全局公共库 `lib` 中引入：`lib/views/monitor-alarm/alarm-panel-manage/render`。

### 1. 基础自动渲染
只需要提供后端的 `uid` 和相关时间/过滤参数，即可以直接依赖后端配置完成图表渲染：

```vue
<template>
  <PanelRender 
    uid="tob_vmp_health_check_gauge" 
    :params="params" 
    :layout="{ rule: false, time: false }" 
    :filterable="false" 
    :panelable="false"
  />
</template>

<script>
// 注意这里的引入路径
import PanelRender from 'lib/views/monitor-alarm/alarm-panel-manage/render'

export default {
  components: { PanelRender },
  computed: {
    params() {
      return { range: 30 * 24 * 3600 } // 例如按秒为单位的时间范围
    }
  }
}
</script>
```

### 2. 局部插槽高度定制图表 (具名劫持渲染)
如果某个特定监控图表在**后端配置时的 `panelType` 被设置为 `7`**（代表自定义组件类型），前端底层的渲染引擎便会主动把控制权下放，暴露以该图表配置项的 `panelKey` 为名称的动态具名插槽。你可以利用此机制（如 `#chart_{ID}` ）进行劫持渲染，并将 `PanelRender` 提炼出的 `context` 传递给自定义组件。

```vue
<PanelRender 
  ref="pr_date" 
  uid="tob_vmp_health_check_bydate" 
  :params="params" 
  :layout="layout"
  :filterable="false" 
  :panelable="false">
  
  <!-- 这里的插槽名严格等同于该子图表在后端配置的唯一标志符 panelKey (例如这里叫 chart_0D7A1A1403) -->
  <template #chart_0D7A1A1403="{ context }">
    <!-- ActiveChart 收到 context 后可以通过其中的 foreignUid, panelKey, scopeId, params 发起自定义请求和重绘 -->
    <ActiveChart :context="context" />
  </template>
  
</PanelRender>
```

在自定义的子组件 `ActiveChart.vue` 中，可利用 `context` 上下文精准组装查询参数：

```javascript
props: { context: Object },
methods: {
  async refresh() {
    // 组装用于二次请求的数据包
    const queryParams = {
        ...this.context.params,
        foreignUid: this.context.uid, // 大盘主 uid
        panelKey: this.context.chart.panelKey // 被劫持图表的具体标识（值为 chart_0D7A1A1403）
    }
    // 注意：必须传入 this.context.scopeId 作为生命周期闭环标志，当 PanelRender 销毁时相关请求可以自动被 abort
    // const res = await getPanelData(queryParams, this.context.scopeId, url)
    // 拿到原始数据后调用 echarts 实例 (this.chartInstance.setOption(...)) 进行渲染
  }
}
```

## 注意事项
1. **外部刷新机制**：如果外部有独立的筛选器，改变条件后可以主动调用 `this.$refs.pr_date.onTimeChange(newRange)` 代为通知；而自定义子组件可以通过注入全局/父级 `eventBus` 并监听 `refresh` 事件（`this.eventBus.on("refresh", this.refresh)`）来实现联动同步刷新。
2. 每一个面板会生成一个包含时间戳的专属 `scopeId` （如 `tob_vmp_xx_1700101111` ），一定要透传给通过 Axios 封装的基础接口，这是项目用于做组件卸载自动 `CancelToken` 拦截的关键。
