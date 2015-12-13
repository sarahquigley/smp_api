# Slot Machine Poetry API Design


## Minimum API Functionality

At a minimum, the slot machine poetry API must offer functionality to:

1. Save submitted words.
2. Retrieve random words.
3. Retrieve sets of words, identified by id.
4. Enable preview of rendered poems via the handwriting.io API.
5. Save poems submitted to the slot machine, including a rendered PNG & PDF of the poem.
6. Retrieve random poems.
7. Retrieve specific poems.


## Development goals

1. Develop API features, excluding any features requiring handwriting.io integration
2. Ready app for deployment and deploy.
3. Integrate handwriting.io, develop API features that require it
4. Ready app for deployment and deploy.

These should be reflected on the client.

## DB Schema

![DB Schema](db-schema.png)

Note: For our initial proof of concept application, rendered poems (png or pdf files) will 
be stored as binary blobs in the database. In the long term, an alternative storage solution 
should be implemented.


## API Endpoints

### Summary

Method  | Endpoint        | Role
--------|-----------------|------------
GET     | /word           | Get words
POST    | /word           | Save word
GET     | /word/random    | Get random word(s)
POST    | /poem           | Save poem
GET     | /poem/{id}      | Get poem
GET     | /poem/{id}/png  | Get poem png
GET     | /poem/{id}/pdf  | Get poem pdf
GET     | /poem/random    | Get random poem
GET     | /poem/preview   | Get poem preview

### Details

#### GET /word - Get word(s)

##### Response (Status 200)

Type: application/json

    [
      {
        "id": 0,
        "word": "string",
        "created_at": "string",
        "modified_at": "string"
      }
    ]

##### Parameters

Parameter   | Value       | Description               | Parameter Type  | Data Type
------------|-------------|---------------------------|-----------------|------------------
pk__in      | (optional)  | ids of words to retrieve  | query           | array of integers


#### POST /word - Save word.

##### Response (Status 200)

Type: application/json

    {
      "id": 0,
      "word": "string",
      "created_at": "string",
      "modified_at": "string"
    }

##### Parameters

Parameter   | Value             | Description           | Parameter Type  | Data Type
------------|-------------------|-----------------------|-----------------|-----------
word        | (required)        | word being saved      | body            | string

#### GET /word/random - Get random word(s)

##### Response (Status 200)

Type: application/json

    [
      {
        "id": 0,
        "word": "string",
        "created_at": "string",
        "modified_at": "string"
      }
    ]

  OR

    {
      ids: [0]
    }

  OR

    [0]

  Just return array of integers and delegate to GET /word for word retrieval?

##### Parameters

Parameter   | Value       | Description               | Parameter Type  | Data Type
------------|-------------|---------------------------|-----------------|-----------
limit       | 3 (default) | number of items to fetch  | query           | integer

#### POST /poem - Save poem

##### Response (Status 200)

Type: application/json

    [
      {
        "id": 0,
        "text": "string",
        "words" : [0]
        "handwriting_id": "string",
        "created_at": "string",
        "modified_at": "string"
      }
    ]

##### Parameters

Parameter       | Value       | Description               | Parameter Type  | Data Type
----------------|-------------|---------------------------|-----------------|------------------
text            | (required)  | poem text                 | body            | string
words           | (optional)  | ids of related words      | body            | array of integers
handwriting_id  | (required)  | id of chosen handwriting  | body            | string

#### GET /poem/{id} - Get poem

##### Response (Status 200)

Type: application/json

    {
      "id": 0,
      "body": "string",
      "handwriting_id": "string",
      "created_at": "string",
      "modified_at": "string"
      "words" : [
        {
          "id": 0,
          "word": "string",
          "created_at": "string",
          "modified_at": "string"
        }
      ]
    }

##### Parameters

Parameter       | Value       | Description | Parameter Type  | Data Type
----------------|-------------|-------------|-----------------|-----------
id              | (required)  | Poem id     | path            | string

#### GET /poem/{id}/png - Get poem png

##### Response (Status 200)

Type: image/png

    Binary image data

##### Parameters

Parameter       | Value       | Description | Parameter Type  | Data Type
----------------|-------------|-------------|-----------------|-----------
id              | (required)  | Poem id     | path            | string


#### GET /poem/{id}/pdf - Get poem pdf

##### Response (Status 200)

Type: application/pdf

    Binary pdf data

##### Parameters

Parameter       | Value       | Description | Parameter Type  | Data Type
----------------|-------------|-------------|-----------------|-----------
id              | (required)  | Poem id     | path            | string


#### GET /poem/random - Get random poem

##### Response (Status 200)

Type: application/json

    {
      "id": 0,
      "body": "string",
      "handwriting_id": "string",
      "created_at": "string",
      "modified_at": "string"
      "words" : [
        {
          "id": 0,
          "word": "string",
          "created_at": "string",
          "modified_at": "string"
        }
      ]
    }

    OR

      {
        ids: [0]
      }

    OR

      [0]

    Just return array of integers and delegate to GET /poem/{id} for poem retrieval?

##### Parameters

None.

#### GET /poem/preview - Get poem preview

##### Response (Status 200)

Type: application/json (?)

    {
      "preview": "base64 encoded string"
    }

##### Parameters

Parameter       | Value       | Description               | Parameter Type  | Data Type
----------------|-------------|---------------------------|-----------------|-----------
body            | (required)  | poem body                 | query           | string
handwriting_id  | (required)  | id of chosen handwriting  | query           | string


# Future Development Ideas

- Spam / pornography prevention
