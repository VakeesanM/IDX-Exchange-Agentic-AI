export interface PropertyFilters {
  city?: string | null;      
  maxPrice?: number | null;  
  beds?: number | null;      
  baths?: number | null;     
  sqft?: number | null;     
  type?: string | null;     
  pool?: "True" | "False" | null;    
  hasView?: "True" | "False" | null; 
}




export interface ListingRow {
  L_ListingID: string;
  L_DisplayId: string;
  L_Address: string;
  L_City: string;
  L_Zip: string;
 
  price: number;          
  beds: number | null;    
  baths: number | null;   
  sqft: number | null;    
  type: string | null;    
  status: string;         
  lat: number | null;     
  lng: number | null;     
 
  YearBuilt: number | null;
  AssociationFee: number | null;  
  DaysOnMarket: number | null;
  PoolPrivateYN: string | null;   
  ViewYN: string | null;
  FireplaceYN: string | null;
  PhotoCount: number | null;
 
  LA1_UserFirstName: string | null;
  LA1_UserLastName: string | null;
  LO1_OrganizationName: string | null;
}

export interface SoldRow {
  ListingKey: number;    
  UnparsedAddress: string;
  City: string;
  CloseDate: string;          
  ClosePrice: number;
  OriginalListPrice: number | null;
  ListPrice: number | null;
  DaysOnMarket: number | null;
 
  BedroomsTotal: number | null;
  BathroomsTotalInteger: number | null;
  LivingArea: number | null;   
 
  PropertyType: string;        
  PropertySubType: string | null;
  YearBuilt: number | null;
 
  ListAgentFullName: string | null;
  ListOfficeName: string | null;
  BuyerOfficeName: string | null;
}