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
  tooltip.className = "tooltip";
};

var hideTooltip = function() {
  var tooltip = this.querySelector("span.tooltip");
  tooltip.className = "tooltip hidden";
};

var extractDoxygenCode = function(node) {
  var lines = node.querySelectorAll("div.code");
  var preText = "";
  for (var i = 0; i < lines.length; i++) {
    var myText = lines[i].textContent;
    preText = preText + myText + "\n";
  }
  return preText;
};

for (var i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener('mouseenter', showTooltip, false);
  buttons[i].addEventListener('mouseleave', hideTooltip, false);
}

window.addEventListener('load', function() {
  var clipboard = new ClipboardJS('.copy-button', {
    text: function(trigger) {
      if (trigger.parentNode.querySelector('td.code')) {
        // var text = extractDoxygenCode(trigger.parentNode);
        var text = trigger.parentNode.querySelector('td.code pre').textContent;
      } else {
        var text = trigger.parentNode.querySelector('pre').textContent;
        
        // if the code snippet represents a console snippet, do not include the '$ ' prefix when copying
        if (trigger.parentNode.querySelector('pre > code[data-lang="console"]')) {
          // apply prefix trimming to each line for multi-line snippets
          text = text.replaceAll(/^\$\s/gm, "");
        }
      }
      return text;
    },
  });

  clipboard.on('success', function(event) {
    event.clearSelection();
    var textEl = event.trigger.querySelector('.copy-button-label');
    var tooltip = event.trigger.querySelector('span.tooltip');
    tooltip.className = "tooltip hidden";
    textEl.textContent = ' Copied!';
    setTimeout(function() {
      textEl.textContent = '';
    }, 2000);
  });

  clipboard.on('error', function (e) {
    console.error('Action:', e.action);
    console.error('Trigger:', e.trigger);
  });
});