# `ef-table` 与 `ef-pagination` 使用规范

## 使用场景
用于业务数据表格结构和底层的翻页。**绝对禁止**擅自使用 `<el-table :data="tableData">`。

## 伪代码骨架
基于双绑定的强规范写法：
```vue
<!-- Table 组件 -->
<ef-table :cols="columns" :rows="tableData">
  <!-- 插槽名必须严格挂接在 cols 定义的 prop 上 -->
  <template #snapshotName="{ row }">
    <el-button type="text">{{ row.snapshotName }}</el-button>
  </template>
  
  <template #operate="{ row }">
    <xx-operate :row="row" @change="getTableData"></xx-operate>
  </template>
</ef-table>

<!-- 分页组件 -->
<ef-pagination :page-sum="pageTotal" :page-set="page" @change="getTableData"></ef-pagination>
```

**`columns` 配表示例结构**：
```javascript
data() {
  return {
    columns: [
      { prop: 'resourceId', label: '资源ID', minWidth: 100 },
      // 对应 template #snapshotName 的自定义插槽列
      { prop: 'snapshotName', label: '快照名称', slotName: 'snapshotName' },
      // 对应 template #operate 的操作列
      { prop: 'operate', label: '操作', width: 120, slotName: 'operate', fixed: 'right' }
    ]
  }
}
```

## 分页跨页勾选场景 (`ef-table-selection`)
当需求涉及到跨越多页的分页勾选操作时，禁止手写复杂的缓存合并逻辑。**必需**配合 `ef-table` 扩展使用 `ef-table-selection` 独立管理选中数据。

### 基本使用骨架
将 `ef-table-selection` 与表格本体相关联，依靠 `ref` 和 `row-key` 属性同步数据：

```vue
<ef-table-selection ref="ets" :table="$refs.table" :selections="rowsData" row-key="desktopId">
  <el-table-column label="云电脑编码" prop="desktopOid"></el-table-column>
  <el-table-column label="云电脑名称" prop="desktopName"></el-table-column>
</ef-table-selection>
<ef-table ref="table" :cols="columns" :rows="tableData" row-key="desktopId" @on-selection="onSelection" v-loading="loading">
  <!-- 运行状态等自定义列 -->
  <template v-slot:useStatus="{row}">
    <ef-status :status="row.useStatus" type="desktop.DESKTOP_USE_STATUS_META"></ef-status>
  </template>
  <template v-slot:vmType="{row}">
    {{ renderVmType(row.vmType) }}
  </template>
</ef-table>
```

> **注意**：`:cols="columns"` 中的 `columns` 是一个数组，由多个对象构成，每个对象需包含 `prop`（字段名）、`label`（显示在表头的中文名称）、及其它配置。如果是自定插槽列，则在 `columns` 中定义 `slotName` 以对应模板内的 `#slotName`。
> 
> **`columns` 示例结构**：
> ```javascript
> data() {
>   return {
>     columns: [
>       { prop: 'desktopName', label: '云电脑名称', minWidth: 120 },
>       { prop: 'ipAddress', label: 'IP地址', minWidth: 140 },
>       // 对应 template #useStatus 的自定义插槽列
>       { prop: 'useStatus', label: '运行状态', slotName: 'useStatus' }
>     ]
>   }
> }
> ```
