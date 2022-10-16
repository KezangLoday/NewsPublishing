	window.onscroll = function () {
			setSticky();
		}

		navbar = document.getElementsByClassName('menu')[0];
		var sticky = navbar.offsetTop;
		function setSticky() {
			if (window.pageYOffset >= sticky) {
				navbar.classList.add('sticky');
			} else {
				navbar.classList.remove('sticky');
			}
		}
