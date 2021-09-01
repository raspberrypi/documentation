var listings = document.querySelectorAll('div.listingblock');

var showButton = function() {
  var button = this.querySelector("button.copy-button");
  button.className = button.className.replace(/\bhidden\b/,'').trim();
};

var hideButton = function() {
  var button = this.querySelector("button.copy-button");
  button.className = button.className + " hidden";
};

for (var i = 0; i < listings.length; i++) {
  listings[i].addEventListener('mouseenter', showButton, false);
  listings[i].addEventListener('mouseleave', hideButton, false);
}

var buttons = document.querySelectorAll('button.copy-button');

var showTooltip = function() {
  var tooltip = this.querySelector("span.tooltip");
  tooltip.className = tooltip.className.replace(/\bhidden\b/,'').trim();
};

var hideTooltip = function() {
  var tooltip = this.querySelector("span.tooltip");
  tooltip.className = tooltip.className + " hidden";
};

for (var i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener('mouseenter', showTooltip, false);
  buttons[i].addEventListener('mouseleave', hideTooltip, false);
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