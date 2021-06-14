$('.btn-share-file').on('click', function() {
	var myModal = new bootstrap.Modal(document.getElementById('shareModal'));
	myModal.show();
	console.log("Modal is now shown");

	const fileId = 'xyz';
	const fileNameSlugified = 'xyz.jpg';

	const permalink = 'http://localhost:27017' + '/download/' + fileId + '/' + fileNameSlugified;

	// 1) This is the javascript way
	document.querySelector('#shareModal .share-link').innerHTML = permalink;
	
	// 2) This is the jquery way
	//$('#shareModal .share-link').html(permalink); 

	
});
