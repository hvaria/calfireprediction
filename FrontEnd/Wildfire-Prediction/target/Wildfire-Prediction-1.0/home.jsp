<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@ include file="firebase.jsp" %>
<!DOCTYPE html>
<html>
    <head>

        <title>Wildfire Prediction</title>
        <link rel="stylesheet" href="css/style.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">        
    </head>
    <body>
        <jsp:include flush="true" page="nav.jsp" />
        <div class="content">
            <h1>Wildfire Prediction</h1>
            <p>Enter two latitude and longitude coordinates, and a date below:</p>
            <br>
            <p style="font-size: 18px;">Bottom left</p>

            <form onsubmit="(event)">

                <div class="longlat-input" style="display:inline-block">
                    <label for="latitude1">Latitude:</label> 
                    <input type="text"
                           id="latitude1" name="latitude1" placeholder="ex. 38.7071">
                </div>
                <div class="longlat-input" style="display:inline-block">
                    <label for="longitude1">Longitude:</label> 
                    <input type="text"
                           id="longitude1" name="longitude1" placeholder="ex. -121.28">
                    <i class="fa fa-question-circle" style="font-size:24px"></i>
                    <div class="info">Input latitude in left boxes and longitude in right side boxes. Latitude
                        <br>
                        decimals range from -90 to 90. Longitude decimals range from -180 to 180.   
                        <br>
                        e.g. Mount Everest coordinates are 27.986065 (Latitude), 86.922623 (Longitude).
                    </div>                      
                </div>

                <br>

                <p style="font-size: 18px;">Top right</p>

                <div class="longlat-input" style="display:inline-block">
                    <label for="latitude2">Latitude:</label> 
                    <input type="text"
                           id="latitude2" name="latitude2" placeholder="ex. 38.7071">
                </div>
                <div class="longlat-input" style="display:inline-block">
                    <label for="longitude2">Longitude:</label> 
                    <input type="text"
                           id="longitude2" name="longitude2" placeholder="ex. -121.28">
                    <i class="fa fa-question-circle" style="font-size:24px"></i>
                    <div class="info">Input latitude in left boxes and longitude in right side boxes. Latitude
                        <br>
                        decimals range from -90 to 90. Longitude decimals range from -180 to 180.   
                        <br>
                        e.g. Mount Everest coordinates are 27.986065 (Latitude), 86.922623 (Longitude).
                    </div>                     
                </div>

                <label for="date">Date:</label> 
                <input type="date" id="date" name="date">


                <br> 


                <div class="button-container">
                    <input type="submit" value="Classify">
                    

                    <div id="fireButtonContainer"></div>
                        <!--<button id="predictionBtn" class="your-button-class" style="display: none;">Run LSTM Prediction</button>-->
                        <button id="predictionBtn" class="fire-detected-btn" style="display: none;">Run LSTM Prediction</button>


                    <div class="loading-overlay">
                        <div class="hourglass-spinner">
                            <div class="upper-part"></div>
                            <div class="lower-part"></div>
                        </div>
                    </div>
                </div>
            </form>

            <button id="save-search" class="save-search">Save Search</button>

            <h4 id="classification"></h4>
            <div class="image-container" id="output_image_div">
                <img id="output_image"/>
            </div>

        </div>         
    </body>
    <script type='module'>
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-app.js";
        import { getDatabase, ref, set, get, update, onValue, child, push} from "https://www.gstatic.com/firebasejs/10.4.0/firebase-database.js";
        import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-auth.js";
        const app = initializeApp(firebaseConfig);
        const database = getDatabase(app);
        const auth = getAuth();
        onAuthStateChanged(auth, (user) => {
            if (!user) {
                window.location.href = "login-page.jsp";
            }

            const currentUserUID = user.uid;
            const currUserRef = ref(database, "users/" + currentUserUID);
            onValue(currUserRef, (snapshot) => {
                const fName = snapshot.val().fName;
                const lName = snapshot.val().lName;
                const firstInitial = fName[0];
            });
        });
        document.querySelector('form').addEventListener('submit', function (event) {
            event.preventDefault();
            document.querySelector(".loading-overlay").style.display = "flex";
            sendRequest();
        });
        async function sendRequest() {
            const url = 'http://localhost:5000/get_classification';
            const formData = new URLSearchParams();
            formData.append('latitude1', document.getElementById('latitude1').value);
            formData.append('longitude1', document.getElementById('longitude1').value);
            formData.append('latitude2', document.getElementById('latitude2').value);
            formData.append('longitude2', document.getElementById('longitude2').value);
            formData.append('date', document.getElementById('date').valueAsDate.toISOString().slice(0, 10));

            try {
                console.log("before fetch");
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData
                });
                console.log("after fetch");
                if (response.ok) {
                    console.log("I am in response.ok");
                    const jsonResponse = await response.json();
                    const classification = jsonResponse.classification;
                    const image = jsonResponse.image;
                    const classificationElement = document.getElementById('classification');
                    classificationElement.innerHTML = classification;
                    const imageElement = document.getElementById('output_image');
                    imageElement.src = 'data:image/jpeg;base64,' + image;
                    const imageContainerDiv = document.getElementById('output_image_div');
                    imageContainerDiv.style.display = 'flex';
                    const saveSearchButton = document.getElementById('save-search');
                    saveSearchButton.style.display = 'inline-block';
                    saveSearchButton.addEventListener('click', saveSearch);
                    if (classification === "Fire Detected") {
                        // Create a button element
                        classificationElement.style.color = "red";
                        const fireButton = document.createElement("button");
                        fireButton.innerText = "Detect";
                        fireButton.className = "fire-detected-btn"; // Assign a class to the button for styling
                        fireButton.addEventListener("click", fetchYoloOutput);
                        
                        // Create the "Prediction" button
//                        const predictionButton = document.createElement("button");
//                        predictionButton.innerText = "Prediction";
//                        predictionButton.className = "fire-detected-btn"; // Use the same class for styling
//                        predictionButton.style.display = 'none'; // Initially hidden
//                        predictionButton.id = "predictionBtn"; // Assign an ID for later use
//                        fireButton.addEventListener("click", sendLSTMRequest());
//                        await sendLSTMRequest();
//                        const lstmButton = document.getElementById("predictionBtn");
//                        lstmButton.style.display = 'inline-block';
//
//                        // Add click event listener to the LSTM button
//                        lstmButton.removeEventListener('click', sendLSTMRequest); // Remove any existing listener
//                        lstmButton.addEventListener('click', sendLSTMRequest);
//                        
                        // Add the button to the fireButtonContainer
                        const fireButtonContainer = document.getElementById("fireButtonContainer");
                        fireButtonContainer.innerHTML = ""; // Clear any existing content
                        fireButtonContainer.appendChild(fireButton);
                        fireButtonContainer.appendChild(predictionButton);
                        
                        
                    } else {
                        // If classification is not "Fire Detected", perform some action
                        const fireButtonContainer = document.getElementById("fireButtonContainer");
                        fireButtonContainer.innerHTML = "<p>No fire detected.</p>";
                        document.getElementById("predictionBtn").style.display = 'none';
                        //                        document.querySelector(".loading-overlay").style.display = "none";
                    }

                    //Hide Spinner
                    document.querySelector(".loading-overlay").style.display = "none";
                } else {
                    console.error("Error during fetch operation", response.status, response.statusText);
                    document.querySelector(".loading-overlay").style.display = "none";
                }
            } catch (error) {
                console.log("I am in error");
                console.error('Error during fetch operation: ', error);
                document.querySelector(".loading-overlay").style.display = "none";
            }

        }

        async function fetchYoloOutput() {
            document.querySelector(".loading-overlay").style.display = "flex";
            fetch('http://localhost:5000/get_yolo_output')
                    .then(response => response.blob())

                    .then(blob => {
                        const url = URL.createObjectURL(blob);
                        const imageElement = document.getElementById('output_image');
                        imageElement.src = url;
                        
                        // Hide the spinner once the YOLO output is received and displayed
                        //                document.querySelector(".loading-overlay").style.display = "none";
                        const lstmButton = document.getElementById("predictionBtn");
                        lstmButton.style.display = 'inline-block';

                        // Add click event listener to the LSTM button
                        lstmButton.removeEventListener('click', sendLSTMRequest); // Remove any existing listener to avoid duplicates
                        lstmButton.addEventListener('click', sendLSTMRequest);

                        // Hide the loading overlay
                        document.querySelector(".loading-overlay").style.display = "none";
                    })
                    .catch(error => {
                        console.error('Error fetching yolo_output.jpg:', error);
                        document.querySelector(".loading-overlay").style.display = "none";
                    });
            document.querySelector(".loading-overlay").style.display = "none";
        }
        
        async function sendLSTMRequest() {
            const url = 'http://localhost:5000/your_lstm_endpoint'; // Replace with the actual URL of your LSTM endpoint
            const formData = new URLSearchParams();
            formData.append('latitude1', document.getElementById('latitude1').value);
            formData.append('longitude1', document.getElementById('longitude1').value);
            formData.append('latitude2', document.getElementById('latitude2').value);
            formData.append('longitude2', document.getElementById('longitude2').value);
            formData.append('date', document.getElementById('date').value);

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    fetchLstmGif();
                    const jsonResponse = await response.json();
                    // Process and display the response from your LSTM model
                } else {
                    console.error("Error during fetch operation", response.status, response.statusText);
                }
            } catch (error) {
                console.error('Error during fetch operation: ', error);
            }
        }
        
        function fetchLstmGif() {
            fetch('http://localhost:5000/get_lstm_gif') // Adjust URL as needed
                .then(response => response.blob())
                .then(blob => {
                    const url = URL.createObjectURL(blob);
                    document.getElementById('output_image').src = url;
                })
                .catch(error => console.error('Error fetching the LSTM GIF:', error));
        }



        function generateUID() {
            // A simple implementation using random numbers
            return (
                    Math.random().toString(36).substr(2, 9) + // Random alphanumeric characters
                    new Date().getTime().toString(36) // Timestamp as alphanumeric characters
                    );
        }

        function saveSearch() {
            console.log("Entering safe search");
            const app = initializeApp(firebaseConfig);
            const database = getDatabase(app);
            const auth = getAuth();
            const lat1 = document.getElementById("latitude1").value;
            const lon1 = document.getElementById("longitude1").value;
            const lat2 = document.getElementById("latitude2").value;
            const lon2 = document.getElementById("longitude2").value;
            const date = document.getElementById("date").value;
            const user = auth.currentUser;
            if (!user) {
                window.location.href = "login-page.jsp";
            } else {
                const currentUserUID = user.uid;
                const searchUID = generateUID();
                const currUserSearchHistoryRef = ref(database, "users/" + currentUserUID + "/search_history");
                get(currUserSearchHistoryRef).then((snapshot)=>{
                 
                
                    if (snapshot.exists()) {
                        console.log('Data exists:', snapshot.val());
                        const search = {
                            searchUID: [
                                {
                                    "lat1": lat1,
                                    "lon1": lon1,
                                    "lat2": lat2,
                                    "lon2": lon2,
                                    "date": date
                                }
                            ]
                        };
                        const newRef = push(currUserSearchHistoryRef);
                        //currUserSearchHistoryRef.push(search);
                        set(newRef, search);
                    } else {
                        console.log('Data does not exist at this path.');
                        const newSearchHistory = {
                            "search_history": [
                                {
                                    searchUID: [
                                        {
                                            "lat1": lat1,
                                            "lon1": lon1,
                                            "lat2": lat2,
                                            "lon2": lon2,
                                            "date": date
                                        }
                                    ]
                                }
                            ]
                        };
                        const newRef = push(currUserSearchHistoryRef);
                        set(newRef, newSearchHistory);
                        //currUserSearchHistoryRef.push(newSearchHistory);
                        //set(ref(database, 'users/' + user.uid), newSearchHistory);

                    }
                });
                
            }

        }



    </script>



</html>