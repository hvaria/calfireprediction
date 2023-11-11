<%-- 
    Document   : login-page
    Created on : Sep 13, 2023, 8:32:10 PM
    Author     : spart
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@ include file="firebase.jsp" %>
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="css/style.css">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>JSP Page</title>
    </head>

<h1 class="title">Wildfire Prediction</h1>
    
<body>
    <div class="centered">
        <h1>Sign Up</h1>
        <div class="sign-up">
            <label for="email">Email</label> 
            <input type="text" id="email" name="username">
        </div>
        <div class="sign-up">
            <label for="firstname">First Name</label> 
            <input type="text" id="firstname" name="firstname">
            <label for="lastname">Last Name</label> 
            <input type="text" id="lastname" name="lastname">
        </div>
        <div class="sign-up">
            <label for="password">Password</label> 
            <input type="password" id="password" name="Password">
            <label for="confirmPassword">Confirm Password</label> 
            <input type="password" id="confirmPassword" name="Confirm Password">
        </div>
        <div class="sign-up">
            <input type="submit" id="signUp" value="Sign Up">
        </div>
        <div>
            <label for="email">Already have an account?</label> 
            <a class="text-link" href="login-page.jsp">Log In</a>
        </div>
    </div>
</body>



  <script type="module">
  import { initializeApp } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-app.js";
  import { getDatabase, ref, set, update  }  from "https://www.gstatic.com/firebasejs/10.4.0/firebase-database.js";
  import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-auth.js";
  
  const app = initializeApp(firebaseConfig);
  const database = getDatabase(app);
  const auth = getAuth();
  
  
  signUp.addEventListener("click", (e) => {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirmPassword").value;
    var firstName = document.getElementById("firstname").value;
    var lastName = document.getElementById("lastname").value;
    
    if (password !== confirmPassword) {
        alert("Passwords do not match. Please try again.");
    }
    else{
    var email = document.getElementById('email').value;
    createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
    // Signed in 
    const user = userCredential.user;
    const json_data = {
    "email": email,
    "fName": firstName,
    "lName": lastName,
    "last_login": new Date().toLocaleString()
  };
    return set(ref(database, 'users/' + user.uid), json_data);
  })
    .then(() => {
        window.location.href = "home.jsp";
    })
     
    .catch((error) => {
      const errorMessage = error.message;
      console.log(errorMessage);
      alert(errorMessage);
      // ..
    });
  }
  });
    
</script>                             



</html>
