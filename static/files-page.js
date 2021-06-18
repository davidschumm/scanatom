function slugify(name) {
	if (!name) {
		return "";
	}


	return name.replace(' ', '-').replace('.', '-').replace('*', '-').replace('+', '-');
};


$('.btn-share-file').on('click', function() {
	const $this = $(this);


	var myModal = new bootstrap.Modal(document.getElementById('shareModal'));
	myModal.show();
	console.log("Modal is now shown");


	const fileId = $this.attr('data-file-id');

	console.log("fileId is: " + fileId);

	const fileName = $this.attr('data-file-name');
	const fileNameSlugified = slugify(fileName);

	const permalink = 'http://localhost:27017' + '/a/' + fileId + '/' + fileNameSlugified;

	console.log("permalink is: " + permalink);

	// 1) This is the javascript way
	document.querySelector('#shareModal .share-link').innerHTML = permalink;
	
	// 2) This is the jquery way
	//$('#shareModal .share-link').html(permalink); 

	
});
