
<nav>
    <div class="user-initials">
        <div class="circle" id="circle"></div>
        <div class="popup-box" id="popupBox">
            <a href="#">Logout</a>
            <a href="#">Search History</a>
        </div>
    </div>
    <ul>
        <li><a href="home.jsp">Home</a></li>
        <li><a href="about.jsp">About</a></li>
        <li><a href="#" id="logOut">Logout</a></li>
        <li><a href="sign-up-page.jsp" id="sign_up">Sign Up</a></li>

    </ul>
</nav>
<script type='module'>
    import { initializeApp } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-app.js";
    import { getAuth, signOut, onAuthStateChanged} from "https://www.gstatic.com/firebasejs/10.4.0/firebase-auth.js";
    import { getDatabase, ref, set, get, update, onValue, child } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-database.js";


    const app = initializeApp(firebaseConfig);
    const auth = getAuth();
    const database = getDatabase(app);

    const logoutButton = document.getElementById('logOut');
    var firstInitial = null;
    var lastInitial = null;

    logoutButton.addEventListener("click", (e) => {
        signOut(auth).then(() => {
            alert('Sign out!');
        }).catch((error) => {

            const errorMessage = error.message;
            alert(errorMessage);
        });
    });


    onAuthStateChanged(auth, (user) => {
        if (!user) {
            window.location.href = "login-page.jsp";
        }

        const currentUserUID = user.uid;
        const currUserRef = ref(database, "users/" + currentUserUID);

        onValue(currUserRef, (snapshot) => {
            const fName = snapshot.val().fName;
            const lName = snapshot.val().lName;
            firstInitial = fName[0];
            lastInitial = lName[0];
            document.getElementById('circle').innerHTML = firstInitial + lastInitial;

        });


    });



    const circle = document.getElementById("circle");
    const popupBox = document.getElementById("popupBox");
    circle.addEventListener("click", function () {
        if (popupBox.style.display === "block") {
            popupBox.style.display = "none";
        } else {
            popupBox.style.display = "block";
        }
    });











</script>