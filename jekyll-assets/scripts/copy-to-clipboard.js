var listings = document.querySelectorAll('div.listingblock');

var showButton = function() {
  var button = this.querySelector("button.copy-button");
  button.className = button.className.replace(/\bhidden\b/,'');
};

var hideButton = function() {
  var button = this.querySelector("button.copy-button");
  button.className = button.className + " hidden";
};

for (var i = 0; i < listings.length; i++) {
  listings[i].addEventListener('mouseenter', showButton, false);
  listings[i].addEventListener('mouseleave', hideButton, false);
}

window.addEventListener('load', function() {
  var clipboard = new ClipboardJS('.copy-button', {
    target: function(trigger) {
      return trigger.parentNode.querySelector('pre');
    },
  });

  clipboard.on('success', function(event) {
    event.clearSelection();
    var textEl = event.trigger.querySelector('.copy-button-label');
    textEl.textContent = ' Copied!';
    setTimeout(function() {
      textEl.textContent = '';
    }, 2000);
  });
});