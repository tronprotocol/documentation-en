function toggleChildren(event) {
  const link = event.currentTarget;
  const nav = link.nextElementSibling;
  const listItem = link.parentElement; // Get the parent <li> element

  if (nav && nav.tagName === 'NAV') {
    // Toggle the expanded/collapsed state
    if (nav.hidden) {
      nav.hidden = false;
      listItem.classList.add('is-expanded'); // Add the is-expanded class
    } else {
      nav.hidden = true;
      listItem.classList.remove('is-expanded'); // Remove the is-expanded class
    }
    //event.preventDefault(); // Prevent the default link behavior
  }
}
