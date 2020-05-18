const AUTH0_AUTHORIZE_URL = "https://udacity-nd-capstone.auth0.com/authorize?audience=casting&response_type=token&client_id=9EalhHTVUmqwMnnF94DT00JuoIHkYtcx&redirect_uri=http://localhost:5000/callback"

function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "menu") {
    x.className += " responsive";
  } else {
    x.className = "menu";
  }
}

window.addEventListener('load', (event) => {
  getHeaders();
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

function GetMovies() {
  console.log('In Get Movies')
  let token = getCookie('jwt_token');
  console.log('GetMovies', token);

  var formData = new FormData();
  var client = new XMLHttpRequest();
  client.open('GET', 'http://localhost:5000/movies');
  const header = client.setRequestHeader('Authorization', `Bearer ${token}`);
  client.send(null);
  return client.responseText;

  $.ajax({
   type : "GET",
   url : "http://localhost:5000/movies",
   beforeSend: function(xhr){xhr.setRequestHeader('Authorization', `Bearer ${token}`);},
   success : function(result) {
       //set your variable to the result
   },
   error : function(result) {
     //handle the error
   }
 });

  // return true;
}
