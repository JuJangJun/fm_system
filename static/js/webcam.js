$(document).ready(function() {
    var video = document.getElementById('video');

    function startWebcam() {
        var url = 'http://192.168.0.174:8080/shot.jpg';

        setInterval(function() {
            fetch(url)
                .then(response => response.blob())
                .then(blob => {
                    var objectURL = URL.createObjectURL(blob);
                    video.src = objectURL;
                })
                .catch(error => console.error('Error:', error));
        }, 100);
    }

    startWebcam();
});
