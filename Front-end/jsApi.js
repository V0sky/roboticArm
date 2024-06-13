function apiRequest(apiURL){
  const fetchPromise = fetch(apiURL);
  
  fetchPromise
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
  }).catch(err => {
    console.log('caught it!',err);
 });
}