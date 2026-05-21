# 只读详情展示规范

## 使用场景

适用于只展示字段、不编辑表单的详情区域，包括：

- 只读详情
- 指标详情
- 页面详情卡片

只读详情是一种独立展示模式，不绑定具体容器。外层容器可以是 `ef-dialog`、抽屉、页面卡片或普通业务区域。

## 推荐结构

字段数量较少、信息以键值展示为主时，优先使用紧凑的两列详情卡片布局。

```vue
<template>
  <div class="readonly-detail">
    <div class="detail-item detail-item--wide">
      <span class="detail-label">桌面编号</span>
      <span class="detail-value">D123456789</span>
    </div>
    <div class="detail-item">
      <span class="detail-label">总登录次数</span>
      <span class="detail-value">10</span>
    </div>
    <div class="detail-item">
      <span class="detail-label">活跃用户数</span>
      <span class="detail-value">20</span>
    </div>
    ...
  </div>
</template>
```

## 推荐样式

```scss
.readonly-detail {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  padding: 4px 16px 8px;
}

.detail-item {
  padding: 10px 14px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  background: #fafafa;
}

.detail-item--wide {
  grid-column: 1 / -1;
}

.detail-label {
  display: block;
  margin-bottom: 6px;
  color: #909399;
  font-size: 13px;
  line-height: 1;
}

.detail-value {
  color: #303133;
  font-size: 16px;
  font-weight: 500;
  line-height: 22px;
  word-break: break-all;
}
```

## 使用原则

- 只读展示不要默认使用 `el-form` 纵向堆字段。
- 不设置 `min-height`，高度跟随内容自然收缩。
- 主标识字段、长字段使用 `detail-item--wide` 占整行。
- 普通指标按两列排列。
- label 使用弱色，value 使用主文本色并适当加粗。
- `v-loading` 可挂在详情容器上，不需要额外包一层空容器。
- 字段缺省展示使用当前项目已有的 `formatText` / `formatNumber` 或同等方法处理。
- 外层容器由具体业务场景决定，不在本规范中限定。