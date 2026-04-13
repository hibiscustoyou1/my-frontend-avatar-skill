# 常量枚举池状态映射规范 (`src/status/*.js` 与 `ef-status`)

## 使用场景
此规范用于规范我们业务体系中所有用于表单翻译和图标指示的底层状态枚举对象定义，并说明在界面上如何结合 `ef-status` 加载渲染。

## 约定格式
在相应的 `src/status/*.status.js` 下的字典必须严格满足 `icon` 及包裹着 `$t` 国际化的 `label`：
```javascript
export const SnapshotStatus = {
  0: { icon: 'el-icon-loading', label: $t('chuang-jian-zhong') },
  1: { icon: 'el-icon-success', label: $t('ke-yong') }
}
```

## 渲染伪代码 (`ef-status`)
当在界面（例如 `ef-table` 的操作列中）需要渲染上述状态时：
```vue
<!-- type 的路径必须指向 status 暴露出的具体常量对象名称 -->
<ef-status :status="row.status" type="volume-snapshot.SnapshotStatus">{{ row.statusName }}</ef-status>
```
