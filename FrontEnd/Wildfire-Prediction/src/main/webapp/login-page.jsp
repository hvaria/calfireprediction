<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@ include file="firebase.jsp" %>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <link rel="stylesheet" href="css/style.css">
        <link rel="stylesheet" href="https://unpkg.com/boxicons@latest/css/boxicons.min.css">
        <title>JSP Page | Login</title>
    </head>
    <h1 class="title">Wildfire Prediction</h1>
    <body>
        
        <div class="centered">
            <h1>Login</h1>
            <div class="log-in">
                <label for="email">Enter Email</label> 
                <input type="text" id="email" name="email">
            </div>		
            <div class="log-in">
                <label for="password">Password</label> 
                <input type="password" id="password" name= "password">
            </div>
            <input type="submit" id = loginIn value="Login">
            <div>
                <label for="email">Don't have an account?</label> 
                <a class="text-link" href="sign-up-page.jsp">Sign Up</a>
            </div>

    </body>

    <script type="module">

        // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-app.js";
  import { getDatabase, ref, set, update  }  from "https://www.gstatic.com/firebasejs/10.4.0/firebase-database.js";
  import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-auth.js";
 
  const app = initializeApp(firebaseConfig);
  const database = getDatabase(app);
  const auth = getAuth();
  
  loginIn.addEventListener("click", (e) => {
      
  var email = document.getElementById('email').value;
  var password = document.getElementById('password').value;
  
  signInWithEmailAndPassword(auth, email, password)
  .then((userCredential) => {
    const user = userCredential.user;
    return update(ref(database, 'users/' + user.uid),{
    last_login : new Date().toLocaleString()
    });
    
  })
    .then(() => {
      window.location.href = "home.jsp";
  })
  .catch((error) => {
    const errorMessage = error.message;
    alert(errorMessage);
  });
  });
</script>    

</html>
