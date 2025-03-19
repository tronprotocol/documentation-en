function toggleChildren(event) {
  const link = event.currentTarget;
  const nav = link.nextElementSibling;
  const listItem = link.parentElement; // 获取父级 <li> 元素

  if (nav && nav.tagName === 'NAV') {
    // 切换展开/折叠状态
    if (nav.hidden) {
      nav.hidden = false;
      listItem.classList.add('is-expanded'); // 添加 is-expanded 类名
    } else {
      nav.hidden = true;
      listItem.classList.remove('is-expanded'); // 移除 is-expanded 类名
    }
    event.preventDefault(); // 阻止默认跳转行为
  }
}
