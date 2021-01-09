tinymce.init({
    selector: '#id_content',
    plugins: 'textcolor save link image media preview codesample contextmenu table code lists fullscreen  insertdatetime  nonbreaking contextmenu directionality searchreplace wordcount visualblocks visualchars code fullscreen autolink lists  charmap print  hr anchor pagebreak',
    toolbar1: 'fullscreen preview | bold italic underline | fontselect fontsizeselect | forecolor backcolor | alignleft alignright aligncenter alignjustify | indent outdent | bullist numlist table  | link image media | codesample | visualblocks visualchars | charmap hr pagebreak nonbreaking anchor | code',
    contextmenu: 'formats | image',

    menubar: true,

    statusbar: true,
    width: 'auto',
    height: 560,

    // enable title field in the Image dialog
    image_title: true,
    // enable automatic uploads of images represented by blob or data URIs
    automatic_uploads: true,
    // add custom filepicker only to Image dialog
    file_picker_types: 'image',
    file_picker_callback: function(cb, value, meta) {
        var input = document.createElement('input');
        input.setAttribute('type', 'file');
        input.setAttribute('accept', 'image/*');

        input.onchange = function() {
            var file = this.files[0];
            var reader = new FileReader();

            reader.onload = function() {
                var id = 'blobid' + (new Date()).getTime();
                var blobCache = tinymce.activeEditor.editorUpload.blobCache;
                var base64 = reader.result.split(',')[1];
                var blobInfo = blobCache.create(id, file, base64);
                blobCache.add(blobInfo);

                // call the callback and populate the Title field with the file name
                cb(blobInfo.blobUri(), {
                    title: file.name
                });
            };
            reader.readAsDataURL(file);
        };

        input.click();
    }
});