document.addEventListener("DOMContentLoaded", function () {
    // Find the parent navigation item containing the TOC
    const tocParentItem = document.querySelector('.md-nav__item--active');

    if (tocParentItem) {
        // Find the <a> element
        const tocLink = tocParentItem.querySelector('.md-nav__link[href="./"]');

        if (tocLink) {
            // Add a click event listener
            tocLink.addEventListener('click', function(event) {
                console.log("Add a click event to collapse the TOC");

                // Check if the TOC is expanded
                if (tocParentItem.classList.contains('md-nav__item--active')) {
                    //console.log("TOC is expanded, executing default behavior first");

                    // Prevent the default behavior
                    event.preventDefault();
                    event.stopPropagation();

                    // Collapse the TOC
                    tocParentItem.classList.remove('md-nav__item--active');
		    window.scrollTo({
			top: 0,
			//behavior: 'smooth' // if necessary, enable smooth jump
	            });

		    
                    // Do not prevent the default behavior, allow page navigation
                    // Execute custom action after the default behavior
                    //setTimeout(() => {
                    //    console.log("Executing custom action after default behavior");

                    //    // Collapse the TOC
                    //    tocParentItem.classList.remove('md-nav__item--active');
                    //    console.log("TOC collapsed by removing 'md-nav__item--active' class");
                    //}, 10); // Delay 0ms to ensure the default behavior executes first
                }
            });
        } else {
            console.error("tocLink not found");
        }
    } 
});
