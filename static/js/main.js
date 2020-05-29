const AUTH0_AUTHORIZE_URL = "https://udacity-nd-capstone.auth0.com/authorize?audience=casting&response_type=token&client_id=9EalhHTVUmqwMnnF94DT00JuoIHkYtcx&redirect_uri=http://localhost:5000/callback"

function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "menu") {
    x.className += " responsive";
  } else {
    x.className = "menu";
  }
}
document.addEventListener("DOMContentLoaded", ready);
function ready() {
  console.log('I am in DOMContentLoaded ready');
  var d = new Date();
  console.log("I am triggered before flask request" + d.toLocaleTimeString());
  // getHeaders();
}
window.addEventListener('load', (event) => {
  console.log('In Load');
  // getHeaders();
  // console.log('page is fully loaded', getHeaders());
  //window.location.href = window.location.href + "?access_token="+ getHeaders();
});
function getHeaders() {
  console.log('getHeaders');
  // console.log(document.cookie);
  let token = getCookie('jwt_token');
  console.log('getHeaders', token);

  var formData = new FormData();
  var client = new XMLHttpRequest();
  client.open('GET', '/movies');
  const header = client.setRequestHeader('Authorization', `Bearer ${token}`);
  client.send(formData);

  // console.log(request.headers)
  // const header = {
  //   headers: new HttpHeaders()
  //     .set('Authorization',  `Bearer ${abcd}`)
  // };

  // alert("in headers");
  // XMLHttpRequest.prototype.origOpen = XMLHttpRequest.prototype.open;
  // XMLHttpRequest.prototype.open   = function () {
  // this.origOpen.apply(this, arguments);
  // const header = {
  //   headers: this.setRequestHeader('Authorization' , `Bearer ${token}`)
  // };
  // return header;
// }
}

function getCookie(name) {
        // Split cookie string and get all individual name=value pairs in an array
        var cookieArr = document.cookie.split(";");

        // Loop through the array elements
        for(var i = 0; i < cookieArr.length; i++) {
            var cookiePair = cookieArr[i].split("=");

            /* Removing whitespace at the beginning of the cookie name
            and compare it with the given string */
            if(name == cookiePair[0].trim()) {
                // Decode the cookie value and return
                return (cookiePair[1]);
            }
        }

        // Return null if not found
        return null;
    }
$(document).ready( function() {
  console.log("In Document Ready");
  let token = getCookie('jwt_token');
  $.ajaxSetup({
    headers:{
      'Authorization': `Bearer ${token}`
    }
  });
  
  //  $('#navMovies').on('click', function(event) {
  //    console.log("in Click");
  //
  //   let token = getCookie('jwt_token');
  //   $.ajaxSetup({
  //     headers:{
  //       'Authorization': `Bearer ${token}`
  //     }
  //   });
  //   $link = $(this);
  //
  //   $.get('http://localhost:5000/movies', {
  //     headers: {'Authorization': `Bearer ${token}`}
  //   })
  //   .done(function(data) {
  //     console.log( "second success", data);
  //     data = data.data
  //     // window.location.replace(window.location.href);
  //     // window.location.href = $link.attr('href');
  //     $(this).html = data.data;
  //   });
  //   console.log('After html');
  //   event.preventDefault();
  //   // $.ajax();
  //   // GetMovies();
  // });
});
// $(document).on("pageinit",function(){
//   GetMovies();
// });

function GetMovies() {
  console.log('In Get Movies');
  // console.log('$link', $link);
  let token = getCookie('jwt_token');
  console.log('GetMovies', token);

  // var formData = new FormData();
  // var client = new XMLHttpRequest();
  // client.open('GET', 'http://localhost:5000/movies');
  // const header = client.setRequestHeader('Authorization', `Bearer ${token}`);
  // client.send();

  // fetch('/movies', {
  //   method: 'GET',
  //   'Content-Type': 'application/json',
  //   redirect: 'manual',
  //   headers: {'Authorization': `Bearer ${token}`}
  // }).then(function (response) {
  //   console.log(response);
  //   // return response.json();
  //   return window.location.href="/movies";
  // });

  $.ajax({
         url: "http://localhost:5000/movies",
         // data: { signature: authHeader },
         type: "GET",
         beforeSend: function(xhr){xhr.setRequestHeader('Authorization', `Bearer ${token}`);},
         headers: {"Authorization": `Bearer ${token}`},
         success: function(result) {
           console.log('Success!'+result);
           // window.location.href = $link.attr('href');
           // document.write(result);
           // window.location="/movies";
         }
      })
      .done(function(response) {
        console.log( "second success", response);
        // window.location.replace(window.location.href);
        // window.location.href = $link.attr('href');
      });
}
