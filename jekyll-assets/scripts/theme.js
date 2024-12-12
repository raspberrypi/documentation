// toggles the site theme between dark and light
function toggleTheme() {
  var cookiePermission = document.cookie.indexOf("cookiebanner_accepted=1");
  
  // fetch the theme from local storage (if it exists)
  var theme = localStorage.getItem('theme');
  // if the theme has never been set, or is light, set the theme to the dark symbol in local storage to change it
  if (localStorage.getItem('theme') !== null && theme == '🌝' ) {
    if (cookiePermission != -1) {
      localStorage.setItem('theme', '🌚');
    }
  } else {
    if (cookiePermission != -1) {
      // otherwise, the theme is currently set to dark, so set the theme to the light symbol in local storage to change it
      localStorage.setItem('theme', '🌝');
    }
  }
  // finally, toggle the light option off or on the body to change the display of the theme
  document.body.classList.toggle('light');
}

// initialises the site theme display
// of key interest here: from the user's perspective, the site defaults to the light theme...
// ...unless your browser uses prefers-color-scheme to ask for a dark theme
// from the site's perspective, we default to a dark theme, but toggle it to a light theme on load if the user doesn't ask for dark.
// why do this? To prevent an annoying light 'flash' for dark theme users. light theme users don't really notice or care if there's a dark anti-flash.
function initTheme() {
  // fetch the theme from local storage (if it exists)
  var theme = localStorage.getItem('theme');
  // if the theme has been set to light (null check to short circuit if not set)
  if(theme !== null && theme === '🌝'
    // if we can use matchMedia and the browser supports the dark color scheme
    || (window.matchMedia && !window.matchMedia('(prefers-color-scheme: dark)').matches)
    && theme !== '🌚') {
      // toggles the theme from the default dark mode to the light version (which actually _shows_ by default to many users)
      document.body.classList.toggle('light');
  }
}