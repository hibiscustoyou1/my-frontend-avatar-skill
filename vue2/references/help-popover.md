# 挂载说明浮窗 (`help-popover`) 规范

## 使用场景
当遇到界面开发中必须提供“悬浮解释”、“禁用的问号点击提示”或其他特定说明文案时必须应用！**绝对不允许**手刻原生的 `title` 属性或者原生的 `el-tooltip` 标签。

## 伪代码参考
```vue
<!-- 基于默认形式的组件补充，默认是一个悬浮图标 -->
<help-popover v-if="btn.help" :width="null">{{ btn.help }}</help-popover>

<!-- 基于包装特定禁用组件的形式以形成更宽广的触发区 -->
<help-popover :width="80">
  <div>在此编写核心的辅助解读说明文案</div>
  <template #icon>
    <el-radio disabled>这是需要被悬浮的目标</el-radio>
  </template>
</help-popover>
```
