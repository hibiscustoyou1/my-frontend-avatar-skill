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
