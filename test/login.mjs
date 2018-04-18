var firebase = require("firebase");

var config = {
    apiKey: "AIzaSyCUnFqUuTmbkyrOQrrskG3jEnoWp-EyJU4",
    authDomain: "dnd-game-manager.firebaseapp.com.firebaseapp.com",
};

firebase.initializeApp(config);

firebase.auth().signInWithEmailAndPassword('mockuser@test.co.za', '123456').catch(function(error) {
    var errorCode = error.code;
    var errorMessage = error.message;
});

firebase.auth().onAuthStateChanged(function(user) {
    if (user) {
      user.getIdToken().then(function(data) {
        console.log(data)
      });
    }
});