/* global global, jest, expect */

const { sendRequest, fetchYoloOutput, generateUID, saveSearch } = window;

describe('sendRequest', () => {
  beforeEach(() => {
    // Mock the fetch function
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ classification: 'Fire Detected', image: 'mockedImageData' })
      })
    );
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('it should send a request and update UI elements', async () => {
    // Set up your form elements
    document.body.innerHTML = `
      <form id="test-form">
        <input id="latitude1" value="38.7071">
        <input id="longitude1" value="-121.28">
        <input id="latitude2" value="38.7071">
        <input id="longitude2" value="-121.28">
        <input id="date" value="2023-10-28">
        <div id="classification"></div>
        <div id="output_image_div" style="display:none;"></div>
        <button id="save-search"></button>
        <div id="fireButtonContainer"></div>
        <div class="loading-overlay"></div>
      </form>
    `;

    // Call your sendRequest function
    await sendRequest();

    // Assert fetch function is called with correct arguments
    expect(fetch).toHaveBeenCalledWith('http://localhost:5000/get_classification', {
      method: 'POST',
      body: expect.any(FormData),
    });

    // Assert UI elements are updated correctly
    expect(document.getElementById('classification').innerHTML).toBe('Fire Detected');
    expect(document.getElementById('output_image_div').style.display).toBe('flex');
    expect(document.getElementById('save-search').style.display).toBe('inline-block');
    expect(document.querySelector('.fire-detected-btn')).not.toBeNull();
  });
});

describe('fetchYoloOutput', () => {
  test('it should fetch YOLO output and update image element', async () => {
    // Mock the fetch function for YOLO output
    global.fetch = jest.fn(() => Promise.resolve(new Blob(['mockedImageData'])));

    // Set up your image element
    document.body.innerHTML = '<img id="output_image">';

    // Call your fetchYoloOutput function
    await fetchYoloOutput();

    // Assert image element src is updated
    expect(document.getElementById('output_image').src).toBe('blob:null/mockedImageData');
  });
});

describe('generateUID', () => {
  test('it should generate a unique ID', () => {
    // Call your generateUID function
    const uid = generateUID();

    // Assert generated UID is not null and has the correct format
    expect(uid).toBeTruthy();
    expect(uid).toMatch(/[a-z0-9]+-[a-z0-9]+/);
  });
});

describe('saveSearch', () => {
  // Mock the Firebase functions and objects if needed

  test('it should save a search', async () => {
    // Set up your form elements
    document.body.innerHTML = `
      <form id="test-form">
        <input id="latitude1" value="38.7071">
        <input id="longitude1" value="-121.28">
        <input id="latitude2" value="38.7071">
        <input id="longitude2" value="-121.28">
        <input id="date" value="2023-10-28">
      </form>
    `;

    // Call the saveSearch function
    await saveSearch();

  });
});


