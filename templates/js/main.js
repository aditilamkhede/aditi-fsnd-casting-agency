function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "menu") {
    x.className += " responsive";
  } else {
    x.className = "menu";
  }
}

// window.addEventListener('load', (event) => {
//   console.log('page is fully loaded');
//   getHeaders();
// });
// getHeaders() {
//   console.log(session['jwt_payload'] )
//   const header = {
//     headers: new HttpHeaders()
//       .set('Authorization',  `Bearer ${abcd}`)
//   };
//   return header;
// }
