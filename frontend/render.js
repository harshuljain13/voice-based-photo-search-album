var name = '';
var encoded = null;
var fileExt = null;
var SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
const synth = window.speechSynthesis;
const recognition = new SpeechRecognition();
const icon = document.querySelector('i.fa.fa-microphone');


function searchFromVoice() {
  recognition.start();

  recognition.onresult = (event) => {
    const speechToText = event.results[0][0].transcript;
    console.log(speechToText);

    document.getElementById("searchbar").value = speechToText;
    search();
  }
}



function search() {
  var searchTerm = document.getElementById("searchbar").value;
  var apigClient = apigClientFactory.newClient({ apiKey: "EiBioXpBIn18FK9nZtntG3il4XqjTqnos8oDWeR8" });

  var params = {
    "q": searchTerm
  };
  var body = {
    "q": searchTerm
  };

  var additionalParams = {
    queryParams: {
      q: searchTerm
    }
  };
  console.log(searchTerm);
  apigClient.searchGet(params, body, additionalParams)
    .then(function (result) {
      console.log('success OK');
      showImages(result.data);
    }).catch(function (result) {
      console.log("Success not OK");
    });
}


function showImages(res) {
  var newDiv = document.getElementById("images");
  if(typeof(newDiv) != 'undefined' && newDiv != null){
  while (newDiv.firstChild) {
    newDiv.removeChild(newDiv.firstChild);
  }
  }
  
  console.log(res);
  if (res.length == 0) {
    var newContent = document.createTextNode("No image to display");
    newDiv.appendChild(newContent);
  }
  else {
    for (var i = 0; i < res.length; i++) {
      console.log(res[i]);
      var newDiv = document.getElementById("images");
      //newDiv.style.display = 'inline'
      var newimg = document.createElement("img");
      var classname = randomChoice(['big', 'vertical', 'horizontal', '']);
      if(classname){newimg.classList.add();}
      newimg.src = res[i];
      newDiv.appendChild(newimg);

      //var currentDiv = document.getElementById("div1");
      //document.body.insertBefore(newDiv, currentDiv);
    }
  }
}

function randomChoice(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}


const realFileBtn = document.getElementById("realfile");
console.log(realFileBtn);

function upload() {
  realFileBtn.click(); 
}

function previewFile(input) {

  var reader = new FileReader();
  name = input.files[0].name;
  console.log(name);
  fileExt = name.split(".").pop();
  var onlyname = name.replace(/\.[^/.]+$/, "");
  var finalName = onlyname + "_" + Date.now() + "." + fileExt;
  name = finalName;

  reader.onload = function (e) {
    var src = e.target.result;
    
    var newImage = document.createElement("img");
    newImage.src = src;
    encoded = newImage.outerHTML;
    console.log(encoded);

    last_index_quote = encoded.lastIndexOf('"');
    if (fileExt == 'jpg' || fileExt == 'jpeg' || fileExt == 'png') {
      encodedStr = encoded.substring(33, last_index_quote);
    }
    else {
      encodedStr = encoded.substring(32, last_index_quote);
    }
    var apigClient = apigClientFactory.newClient({ apiKey: "EiBioXpBIn18FK9nZtntG3il4XqjTqnos8oDWeR8" });

    var params = {
      "key": name,
      "bucket": "voicealbumb2",
      "Content-Type": "image/jpg;base64"

    };

    var additionalParams = {
      headers: {
      }
    };
    console.log(encodedStr);
    apigClient.uploadBucketKeyPut(params, encodedStr, additionalParams)
      .then(function (result) {
        console.log('success OK');
      }).catch(function (result) {
        console.log(result);
      });
  }
  reader.readAsDataURL(input.files[0]);
}
