--Standardizing Date Format
ALTER TABLE CleaningPortfolioProject..NashvilleHousing
ADD SaleDateConverted date;

UPDATE CleaningPortfolioProject..NashvilleHousing
SET SaleDateConverted = CAST(SaleDate AS date)

ALTER TABLE CleaningPortfolioProject..NashvilleHousing
DROP COLUMN SaleDate

--Populating Property Address
SELECT a.ParcelID, b.ParcelID, a.PropertyAddress, b.PropertyAddress, ISNULL(a.PropertyAddress, b.PropertyAddress)
FROM CleaningPortfolioProject..NashvilleHousing a
JOIN CleaningPortfolioProject..NashvilleHousing b
   ON a.ParcelID = b.ParcelID 
   AND a.[UniqueID ] <> b.[UniqueID ]
WHERE a.PropertyAddress IS NULL

UPDATE a 
SET PropertyAddress = ISNULL(a.PropertyAddress, b.PropertyAddress)
FROM CleaningPortfolioProject..NashvilleHousing a
JOIN CleaningPortfolioProject..NashvilleHousing b
   ON a.ParcelID = b.ParcelID 
   AND a.[UniqueID ] <> b.[UniqueID ]
WHERE a.PropertyAddress IS NULL

--Seprating City Name From Address
SELECT PropertyAddress, 
	   SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress) - 1) AS Address,
       SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress) + 1, LEN(PropertyAddress)-(CHARINDEX(',', PropertyAddress) + 1)) AS City
FROM CleaningPortfolioProject..NashvilleHousing

ALTER TABLE CleaningPortfolioProject..NashvilleHousing
ADD Address nvarchar(255), City nvarchar(255)

UPDATE CleaningPortfolioProject..NashvilleHousing
SET Address = SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress) - 1),
	City = SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress) + 1, LEN(PropertyAddress)-(CHARINDEX(',', PropertyAddress) + 1))

--PARSING Owner Address
SELECT PARSENAME(REPLACE(OwnerAddress, ',', '.'), 3),
	   PARSENAME(REPLACE(OwnerAddress, ',', '.'), 2),
	   PARSENAME(REPLACE(OwnerAddress, ',', '.'), 1)
FROM CleaningPortfolioProject..NashvilleHousing

ALTER TABLE CleaningPortfolioProject..NashvilleHousing
ADD OwnerSplitAddress nvarchar(255), OwnerCity nvarchar(255), OwnerState nvarchar(255)

UPDATE CleaningPortfolioProject..NashvilleHousing
SET OwnerSplitAddress = PARSENAME(REPLACE(OwnerAddress, ',', '.'), 3),
	OwnerCity = PARSENAME(REPLACE(OwnerAddress, ',', '.'), 2),
	OwnerState = PARSENAME(REPLACE(OwnerAddress, ',', '.'), 1)

--Remove Y or N in SoldAsVacant
SELECT SoldAsVacant, COUNT(SoldAsVacant)
FROM CleaningPortfolioProject..NashvilleHousing
GROUP BY SoldAsVacant
ORDER BY 2

UPDATE CleaningPortfolioProject..NashvilleHousing
SET SoldAsVacant = CASE WHEN SoldAsVacant = 'Y' THEN 'YES'
					    WHEN SoldAsVacant = 'N' THEN 'NO'
				        ELSE SoldAsVacant END

--Removing Duplicate rows and unused columns
WITH DuplicateRowNumber AS
(
SELECT *, ROW_NUMBER() OVER(PARTITION BY ParcelID, PropertyAddress, SalePrice, SaleDate, LegalReference
                         ORDER BY UniqueID) AS DuplicateRow
FROM CleaningPortfolioProject..NashvilleHousing
)

DELETE
FROM DuplicateRowNumber
WHERE DuplicateRow > 1

ALTER TABLE CleaningPortfolioProject..NashvilleHousing
DROP COLUMN OwnerAddress, TaxDistrict, PropertyAddress



