chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
      if (request.action === "grabUrlAndTimestamp") {
        // Pause the video
        var video = document.querySelector('video.video-stream.html5-main-video');
        video.pause();
    
        // Grab the video URL and current timestamp
        var url = window.location.href;
        var timestamp = video.currentTime;
    
        // Send back the URL and timestamp to the popup script
        sendResponse({ url: url, timestamp: timestamp });
      }
    });
    