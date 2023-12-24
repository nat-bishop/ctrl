CREATE TABLE Assets (
    AssetID SERIAL PRIMARY KEY,
    AssetPath VARCHAR(255) NOT NULL UNIQUE,
    ThumbnailPath VARCHAR(255) NULL,
    ViewingPath VARCHAR(255),
    Type VARCHAR(50) NOT NULL,
    Title VARCHAR(100) NOT NULL,
    Description TEXT NOT NULL,
    Mediator VARCHAR(100),
    DateCreated DATE,
    Rights TEXT NOT NULL
);

CREATE TABLE Projects (
    ProjectID SERIAL PRIMARY KEY,
    PayloadPath VARCHAR(255) PRIMARY KEY ,
    Title VARCHAR(100) NOT NULL UNIQUE,
    Description TEXT,
    DateCreated DATE
);

CREATE TABLE Asset_Projects (
    AssetID INT,
    ProjectID INT,
    FOREIGN KEY (AssetID) REFERENCES Assets(AssetID),
    FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID)
);

CREATE TABLE Asset_Parts (
    ParentAssetID INT,
    PartAssetID INT,
    FOREIGN KEY (ParentAssetID) REFERENCES Assets(AssetID),
    FOREIGN KEY (PartAssetID) REFERENCES Assets(AssetID)
);

CREATE TABLE Asset_Variations (
    OriginalAssetID INT,
    VariationAssetID INT,
    VariationDescription TEXT,
    FOREIGN KEY (OriginalAssetID) REFERENCES Assets(AssetID),
    FOREIGN KEY (VariationAssetID) REFERENCES Assets(AssetID)
);

CREATE TABLE Tags (
    TagID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL
);

CREATE TABLE Asset_Tags (
    AssetID INT,
    TagID INT,
    FOREIGN KEY (AssetID) REFERENCES Assets(AssetID),
    FOREIGN KEY (TagID) REFERENCES Tags(TagID)
);

CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Bio TEXT
);

CREATE TABLE Asset_Users (
    AssetID INT,
    UserID INT,
    FOREIGN KEY (AssetID) REFERENCES Assets(AssetID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Project_Users (
    ProjectID INT,
    UserID INT,
    FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);