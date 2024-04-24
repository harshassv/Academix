document.addEventListener('DOMContentLoaded', function() {
    var summarizeButton = document.getElementById('summarize');
    console.log(summarizeButton)
    var explainButton = document.getElementById('examples');
    var funnyButton = document.getElementById('funny');
    var kidButton = document.getElementById('kid');
    var professionalButton = document.getElementById('professional');
    var expandButton = document.getElementById('expand');

    var humorButton = document.getElementById('humor');
    var shakespeareButton = document.getElementById('shakespeare');
    var storyButton = document.getElementById('story');
    var bulletpointsButton = document.getElementById('bulletPoints');
    var simpleButton = document.getElementById('simple');
    var technicalsimplerButton = document.getElementById('technicalSimpler');

    summarizeButton.addEventListener('click', function() {
      console.log('button clicked')
      chrome.runtime.sendMessage({action: "summarize"});
    });
  
    explainButton.addEventListener('click', function() {
      chrome.runtime.sendMessage({action: "examples"});
    });

    funnyButton.addEventListener('click', function() {
      chrome.runtime.sendMessage({action: "funny"});
    });

    kidButton.addEventListener('click', function() {
      chrome.runtime.sendMessage({action: "explain"});
    });

    professionalButton.addEventListener('click', function() {
      chrome.runtime.sendMessage({action: "professional"});
    });

    expandButton.addEventListener('click', function() {
      chrome.runtime.sendMessage({action: "expand"});
    });

    humorButton.addEventListener('click', function() {
      chrome.runtime.sendMessage({action: "humor"});
    });

    shakespeareButton.addEventListener('click', function() {
      chrome.runtime.sendMessage({action: "shakespeare"});
    });

    storyButton.addEventListener('click', function() {
      chrome.runtime.sendMessage({action: "story"});
    });

    bulletpointsButton.addEventListener('click', function() {
      chrome.runtime.sendMessage({action: "bulletPoints"});
    });

    simpleButton.addEventListener('click', function() {
      chrome.runtime.sendMessage({action: "simple"});
    });

    technicalsimplerButton.addEventListener('click', function() {
      chrome.runtime.sendMessage({action: "technicalSimpler"});
    });
  });

  