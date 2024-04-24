var activeTab;

document.getElementById('grabButton').addEventListener('click', function() {

  var entered_query = textInput.value;
  console.log(entered_query)

  this.style.display = 'none';
  var iframe = document.getElementById('myIframe');
        iframe.style.display = 'block';
        iframe.src = 'http://127.0.0.1:7860/';
        // iframe.width = 1200;
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    activeTab = tabs[0];
    var data;
      console.log(activeTab);
      console.log(activeTab.url);


      if (activeTab.url.includes("youtube")) {
        console.log('youbjdbsf')
        data = {
          url: activeTab.url,
          // timestamp: response.timestamp
          title: activeTab.title
        };
        console.log(data);
      }
      else if (activeTab.url.includes("github")) {
        console.log('github');
        var parts = activeTab.url.split("/");
      var repoName = parts[parts.length - 1];
        data = {
          url: activeTab.url,
          repo_name : repoName,
          query: entered_query
        };
        console.log(data);
      }else {
        console.log('other');
        data = {
          url: activeTab.url,
          query: entered_query
        };
      }
     
      
      // Make a POST request to your FastAPI endpoint
      fetch('http://localhost:5000/receive_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(data => {
        console.log('Received response from server:', data);
        // Handle the response from the server as needed
      })
      .catch(error => {
        console.error('Error:', error);
        // Handle errors if any
      });

  });
    // chrome.tabs.sendMessage(activeTab.id, { action: "grabUrlAndTimestamp" }, function(response) {
      
      
      // document.getElementById('urlDisplay').textContent = response.url;
      // document.getElementById('timestampDisplay').textContent = response.timestamp;
      
    });

// });