# 标准模态弹层 (`ef-dialog`) 规范

## 使用场景
适用于所有的编程式新建、编辑、确认相关的浮层操作。

## 伪代码骨架
该组件直接包裹表单逻辑即可，但所有操作按键必须位于内部插槽内。
```vue
<template>
  <ef-dialog>
    <!-- 弹层直接开始刻画表单结构 -->
    <el-form ref="form" :model="formData" :rules="rules" label-width="100px">
      ...
    </el-form>
    
    <!-- 操作区按钮一定要放到 footer 插槽中 -->
    <template #footer>
      <el-button @click="$emit('on-close')">{{ $t('qu-xiao') }}</el-button>
      <el-button type="primary" :loading="loadings.submit" @click="onConfirm">{{ $t('que-ding') }}</el-button>
    </template>
  </ef-dialog>
</template>
```
