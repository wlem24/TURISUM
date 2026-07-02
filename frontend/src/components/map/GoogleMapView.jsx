import { useMemo } from "react";
import { GoogleMap, LoadScript, MarkerF } from "@react-google-maps/api";
import { useLanguage } from "@/contexts/LanguageContext";

// Athar (أثر) dark-green map skin — matches the app's brand ramp.
const ATHAR_MAP_STYLES = [
  { elementType: "geometry", stylers: [{ color: "#EAF3DE" }] },
  { elementType: "labels.text.stroke", stylers: [{ color: "#F5F2EC" }] },
  { elementType: "labels.text.fill", stylers: [{ color: "#27500A" }] },
  { featureType: "road", elementType: "geometry", stylers: [{ color: "#FFFFFF" }] },
  { featureType: "road", elementType: "geometry.stroke", stylers: [{ color: "#C0DD97" }] },
  { featureType: "water", elementType: "geometry", stylers: [{ color: "#97C459" }] },
  { featureType: "poi", elementType: "geometry", stylers: [{ color: "#C0DD97" }] },
  { featureType: "administrative", elementType: "geometry.stroke", stylers: [{ color: "#97C459" }] },
];

const MAP_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
const isKeyConfigured = MAP_KEY && MAP_KEY !== "your-google-maps-api-key";

export default function GoogleMapView({ lat, lng, title, zoom = 12, height = 320 }) {
  const { isArabic } = useLanguage();
  const center = useMemo(() => ({ lat, lng }), [lat, lng]);

  if (lat == null || lng == null) return null;

  if (!isKeyConfigured) {
    return (
      <div
        style={{ height }}
        className="rounded-xl border border-gray-100 bg-gray-50 flex flex-col items-center justify-center text-center gap-2 text-gray-400 text-sm px-4"
      >
        <span className="text-3xl">🗺️</span>
        <span>
          {isArabic
            ? "أضف VITE_GOOGLE_MAPS_API_KEY في frontend/.env لعرض الخريطة التفاعلية"
            : "Add VITE_GOOGLE_MAPS_API_KEY in frontend/.env to enable the interactive map"}
        </span>
      </div>
    );
  }

  return (
    <div style={{ height }} className="rounded-xl overflow-hidden border border-gray-100">
      <LoadScript googleMapsApiKey={MAP_KEY} language={isArabic ? "ar" : "en"} region="SA">
        <GoogleMap
          mapContainerStyle={{ width: "100%", height: "100%" }}
          center={center}
          zoom={zoom}
          options={{
            styles: ATHAR_MAP_STYLES,
            disableDefaultUI: true,
            zoomControl: true,
            streetViewControl: false,
            fullscreenControl: true,
          }}
        >
          <MarkerF position={center} title={title} />
        </GoogleMap>
      </LoadScript>
    </div>
  );
}
