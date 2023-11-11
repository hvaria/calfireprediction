/* global jest */

// Import required modules using CommonJS syntax
const { signInWithEmailAndPassword } = require('./firebase.jsp');
require('./setupTests.js');

// Import Jest testing utilities
import { act, fireEvent, screen } from "@testing-library/dom";
import "@testing-library/jest-dom/extend-expect";

// Mock the Firebase signInWithEmailAndPassword function
jest.mock("./firebase.jsp", () => ({
  signInWithEmailAndPassword: jest.fn()
}));

describe("Login Page", () => {
  test("should call signInWithEmailAndPassword with correct email and password", async () => {
    // Arrange: Set up the DOM elements
    document.body.innerHTML = `
      <input type="text" id="email" />
      <input type="password" id="password" />
      <button id="loginBtn">Login</button>
    `;

    // Act: Interact with the DOM elements
    await act(async () => {
      fireEvent.change(screen.getByLabelText(/Enter Email/i), {
        target: { value: "test@example.com" }
      });
      fireEvent.change(screen.getByLabelText(/Password/i), {
        target: { value: "password123" }
      });

      fireEvent.click(screen.getByText(/Login/i));
    });

    // Assert: Check if the signInWithEmailAndPassword function is called correctly
    expect(signInWithEmailAndPassword).toHaveBeenCalledWith(
      expect.any(Object), // Firebase auth object
      "test@example.com",
      "password123"
    );
  });
});

