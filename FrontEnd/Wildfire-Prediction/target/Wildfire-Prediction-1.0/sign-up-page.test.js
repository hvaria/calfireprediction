/* global jest */

// Import necessary functions and libraries for testing
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-app.js";
import { getDatabase, ref, set } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-database.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-auth.js";

/// Import the necessary functions and objects for testing
import { createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-auth.js";

// Import Jest testing utilities
import { act, fireEvent, screen } from "@testing-library/dom";
import "@testing-library/jest-dom/extend-expect";

// Mock the Firebase createUserWithEmailAndPassword function
jest.mock("./firebase.jsp", () => ({
  createUserWithEmailAndPassword: jest.fn()
}));

describe("Unit Test for signUp function", () => {
  it("should create a new user and redirect to home page on successful sign-up", () => {
    // Mock the necessary elements and values for the test
    document.getElementById = jest.fn((id) => {
      if (id === "email") {
        return { value: "test@email.com" };
      } else if (id === "password123") {
        return { value: "password123" };
      } else if (id === "password123") {
        return { value: "password123" };
      } else if (id === "John") {
        return { value: "John" };
      } else if (id === "Doe") {
        return { value: "Doe" };
      }
    });

    // Call the signUp function
    signUp();

    // Assert that the necessary Firebase function was called
    expect(createUserWithEmailAndPassword).toHaveBeenCalledWith({}, "test@email.com", "password123");

  });

  it("should display an error message on password mismatch", () => {
    // Mock the necessary elements and values for the test
    document.getElementById = jest.fn((id) => {
      if (id === "email") {
        return { value: "test@email.com" };
      } else if (id === "password123") {
        return { value: "password123" };
      } else if (id === "password123") {
        return { value: "password321" };
      }
    });

    // Mock the alert function
    const mockAlert = jest.fn();
    global.alert = mockAlert;

    // Call the signUp function
    signUp();

    // Assert that an error message is displayed
    expect(mockAlert).toHaveBeenCalledWith("Passwords do not match. Please try again.");
  });
});
