# `ef-condition` 与 `ef-search` 使用规范

## 使用场景
当开发带有条件检索、带有操作按钮区的表格顶部布局时读取此组件。

## 伪代码骨架
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
      <!-- attach 动态并入已定义的 formData 中 -->
      <ef-search :conditions="conditions" :attach="formData"></ef-search>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="getTableData()">查询</el-button>
    </el-form-item>
  </template>
</ef-condition>
```
