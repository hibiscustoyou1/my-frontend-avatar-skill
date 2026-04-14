# `ef-table` 与 `ef-pagination` 使用规范

## 使用场景
用于业务数据表格结构和底层的翻页。**绝对禁止**擅自使用 `<el-table :data="tableData">`。

## 伪代码骨架
基于双绑定的强规范写法：

> **注意**：`:cols="columns"` 中的 `columns` 是一个数组，由多个对象构成，每个对象需包含 `prop`（字段名）、`label`（显示在表头的中文名称）、及其它 `el-table` 配置。

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
      // 对应 template #snapshotName 的自定义插槽列，语法为 #{prop}
      { prop: 'snapshotName', label: '快照名称' },
      // 对应 template #operate 的操作列
      { prop: 'operate', label: '操作', width: 120, fixed: 'right' }
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
<ef-table ref="table" :cols="columns" :rows="tableData" row-key="desktopId" @selection-change="onSelection" v-loading="loading">
  <!-- 运行状态等自定义列 -->
  <template #useStatus="{row}">
    <ef-status :status="row.useStatus" type="desktop.DESKTOP_USE_STATUS_META"></ef-status>
  </template>
  <template #vmType="{row}">
    {{ renderVmType(row.vmType) }}
  </template>
</ef-table>
```

> **`columns` 示例结构**：
> ```javascript
> data() {
>   return {
>     columns: [
>       { prop: 'desktopName', label: '云电脑名称', minWidth: 120 },
>       { prop: 'ipAddress', label: 'IP地址' },
>       { prop: 'useStatus', label: '运行状态' }
>     ]
>   }
> }
> ```

## 行合并与表头合并

当需要将表格的某些行数据根据相同的标识合并，或者实现多级嵌套表头的时候，可以直接通过配置实现。

### 基本使用骨架

在 `ef-table` 中配置 `need-merge` 开启行合并开关，并提供 `children-prop` （例如 `subjects`，不填默认为 `children`）指出作为子级循环的数据键名。同时需要在 `columns` 的对应列设置中配置 `subjects`（默认为 `children`） 数组来实现多层表头的合并展示。

```vue
<template>
  <ef-table :rows="tableData" :cols="columns" need-merge children-prop="subjects"></ef-table>
</template>

<script>
export default {
  data() {
    return {
      columns: [
        { prop: 'id', label: 'ID' },
        { prop: 'name', label: '姓名' },
        { prop: 'subject', label: '科目' },
      ],
      tableData: [
        {
          id: '10001',
          name: '王小虎',
          subjects: [
            { subject: '语文' },
            // ... 代表基于同一主键（如 id=10001）需要行合并的子级数据集合
          ]
        },
        // ... 更多外部主体数据
      ]
    }
  }
}
</script>
```
