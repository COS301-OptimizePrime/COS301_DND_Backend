var firebase = require("firebase");

var config = {
    apiKey: "AIzaSyCUnFqUuTmbkyrOQrrskG3jEnoWp-EyJU4",
    authDomain: "dnd-game-manager.firebaseapp.com.firebaseapp.com",
};

firebase.initializeApp(config);

var user = 'mockuser@test.co.za'

if (process.argv.length >= 3) {
    user = process.argv[2].trim();
}

firebase.auth().signInWithEmailAndPassword(user, '123456').catch(function(error) {
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