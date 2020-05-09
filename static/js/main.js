function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "menu") {
    x.className += " responsive";
  } else {
    x.className = "menu";
  }
}

window.addEventListener('load', (event) => {
  console.log('page is fully loaded');
  getHeaders();
});
function getHeaders() {
  // console.log(document.cookie);
  // var formData = new FormData();
  // var client = new XMLHttpRequest();
  // client.open('GET', '/');
  // client.setRequestHeader('Authorization', document.cookie['jwt_token']);
  // client.send(formData);

  // console.log(request.headers)
  // const header = {
  //   headers: new HttpHeaders()
  //     .set('Authorization',  `Bearer ${abcd}`)
  // };


  // XMLHttpRequest.prototype.origOpen = XMLHttpRequest.prototype.open;
  // XMLHttpRequest.prototype.open   = function () {
  // this.origOpen.apply(this, arguments);
  // this.setRequestHeader('Authorization' , 'Bearer ' + document.cookie['jwt_token']);
  // };
  // return header;
}
