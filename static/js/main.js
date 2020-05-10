function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "menu") {
    x.className += " responsive";
  } else {
    x.className = "menu";
  }
}

window.addEventListener('load', (event) => {
  console.log('page is fully loaded', window.location.href);
  // window.location.href = window.location.href + "?access_token="+ getHeaders();
});
function getHeaders() {
  // console.log(document.cookie);
  var formData = new FormData();
  var client = new XMLHttpRequest();
  client.open('GET', '/');
  let token = getCookie('jwt_token');
  console.log(token);
  const header = client.setRequestHeader('Authorization', token);
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
  // this.setRequestHeader('Authorization' , 'Bearer ' + document.cookie['jwt_token']);
  // };
  return header;
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
