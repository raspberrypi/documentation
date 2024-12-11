var coverImages = document.querySelectorAll('.whitepaper div.coverimage');

for (var i = 0; i < coverImages.length; i++) {
  coverImages[i].addEventListener('click', clickCover, false);
}

function clickCover() {
	var url = this.getAttribute("data-link");
	window.open(url);
}