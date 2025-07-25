def test_index_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Sophia" in response.data
    assert b"Login" in response.data
    assert b"Register" in response.data

def test_protected_page_redirects(client):
    """
    GIVEN a Flask application configured for testing
    WHEN a protected page (e.g., /collections) is requested by an anonymous user
    THEN check that the user is redirected to the login page
    """
    response = client.get('/collections', follow_redirects=True)
    assert response.status_code == 200
    # Check that the redirected page is the login page
    assert b"Sign In" in response.data
    assert b"Username" in response.data
