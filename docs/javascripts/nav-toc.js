document.addEventListener("DOMContentLoaded", function () {
    // 找到包含 TOC 的父导航项
    const tocParentItem = document.querySelector('.md-nav__item--active');

    if (tocParentItem) {
        // 找到 <a> 元素
        const tocLink = tocParentItem.querySelector('.md-nav__link[href="./"]');

        if (tocLink) {
            // 添加点击事件监听器
            tocLink.addEventListener('click', function(event) {
                console.log("add an click event to collapse toc");

                // 检查 TOC 是否已展开
                if (tocParentItem.classList.contains('md-nav__item--active')) {
                    //console.log("TOC is expanded, executing default behavior first");

                    // 阻止默认行为
                    event.preventDefault();
                    event.stopPropagation();

                    // 折叠 TOC
                    tocParentItem.classList.remove('md-nav__item--active');
		    // 不阻止默认行为，允许页面跳转
                    // 在默认行为完成后执行自定义事件
                    //setTimeout(() => {
                    //    console.log("Executing custom action after default behavior");

                    //    // 折叠 TOC
                    //    tocParentItem.classList.remove('md-nav__item--active');
                    //    console.log("TOC collapsed by removing 'md-nav__item--active' class");
                    //}, 10); // 延迟 0ms，确保默认行为先执行
                }
            });
        } else {
            console.error("tocLink not found");
        }
    } else {
        console.error("tocParentItem not found");
    }
});
