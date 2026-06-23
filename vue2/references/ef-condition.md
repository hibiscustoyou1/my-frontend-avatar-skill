# `ef-condition` 与 `ef-search` 使用规范

## 使用场景
当开发带有条件检索、带有操作按钮区的表格顶部布局时读取此组件。

## `ef-condition` 伪代码骨架
```vue
<ef-condition>
  <template #left>
    <!-- 左侧一般预留给新建、删除等主操作按钮，必须使用 el-form-item 进行定宽与对齐包裹 -->
    <el-form-item>
      <el-button type="primary">新建</el-button>
    </el-form-item>
  </template>
  <template #right>
    <el-form-item>
      <ef-search :conditions="conditions" :attach="formData" append-search @search="onSearch"></ef-search>
    </el-form-item>
    <el-form-item>
      <el-button icon="el-icon-refresh" @click="getTableData()"></el-button>
    </el-form-item>
  </template>
</ef-condition>
```

---

## `ef-search` 独立用法

当搜索组件不嵌套在 `ef-condition` 内，而是独立放置于页面某区域时，直接使用 `ef-search`。

### Props 说明

| Prop | 类型 | 说明 |
|------|------|------|
| `conditions` | `Array<{field, label}>` | 搜索条件配置，field 对应 formData 字段名，label 为下拉选项文案 |
| `attach` | `Object` | 绑定的表单数据对象，搜索输入会同步写入此对象 |
| `append-search` | `Boolean` | 是否在输入框后追加搜索按钮 |
| `disabled` | `Boolean` | 禁用搜索组件 |

### Events

| Event | 说明 |
|-------|------|
| `@search` | 点击搜索按钮或回车时触发，通常在此重置分页并调用列表接口 |

### 完整示例

```vue
<template>
  <ef-search
    :conditions="conditions"
    :attach="formData"
    append-search
    @search="onSearch"
  ></ef-search>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        desktopCode: "",
        desktopNickName: "",
      },
      conditions: [
        { field: "desktopCode", label: "桌面编号" },
        { field: "desktopNickName", label: "桌面别名" },
      ],
      page: { pageNum: 1, pageSize: 10 },
    };
  },
  methods: {
    onSearch() {
      this.page.pageNum = 1;
      this.getTableData();
    },
    async getTableData() {
      const params = {
        ...this.page,
        desktopCode: this.formData.desktopCode.trim(),
        desktopNickName: this.formData.desktopNickName.trim(),
      };
      // 调用 API...
    },
  },
};
</script>
```

### 禁用状态

```vue
<ef-search
  :conditions="conditions"
  :attach="formData"
  :disabled="isDisabled"
  append-search
  @search="onSearch"
></ef-search>
```
