import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import PageWrapper from "@/components/layout/PageWrapper";
import { adminAPI } from "@/api/admin";
import { spotsAPI } from "@/api/spots";
import { useLanguage } from "@/contexts/LanguageContext";
import Spinner from "@/components/common/Spinner";
import Button from "@/components/common/Button";
import Badge from "@/components/common/Badge";
import toast from "react-hot-toast";

export default function PendingSpots() {
  const { isArabic } = useLanguage();
  const queryClient = useQueryClient();
  const [rejectionReason, setRejectionReason] = useState({});
  const [processing, setProcessing] = useState({});

  const { data: spots, isLoading } = useQuery({
    queryKey: ["pending-spots"],
    queryFn: () => adminAPI.getPendingSpots({}).then((r) => r.data),
  });

  const handleApproval = async (spotId, approved) => {
    setProcessing((prev) => ({ ...prev, [spotId]: true }));
    try {
      await spotsAPI.approve(spotId, {
        approved,
        rejection_reason: approved ? undefined : rejectionReason[spotId],
      });
      toast.success(isArabic
        ? (approved ? "تمت الموافقة على الموقع ✅" : "تم رفض الموقع")
        : (approved ? "Spot approved ✅" : "Spot rejected"));
      queryClient.invalidateQueries({ queryKey: ["pending-spots"] });
    } catch (err) {
      toast.error(err.response?.data?.detail || "Error");
    } finally {
      setProcessing((prev) => ({ ...prev, [spotId]: false }));
    }
  };

  return (
    <PageWrapper>
      <div className="mb-8">
        <h1 className="page-title">{isArabic ? "المواقع بانتظار الموافقة ⏳" : "Pending Spots Review ⏳"}</h1>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-20"><Spinner size="lg" /></div>
      ) : !spots?.length ? (
        <div className="text-center py-20 text-gray-400">
          <div className="text-5xl mb-4">✅</div>
          <p className="text-lg font-medium">{isArabic ? "لا توجد مواقع بانتظار المراجعة" : "No pending spots"}</p>
        </div>
      ) : (
        <div className="space-y-6">
          {spots.map((spot) => (
            <div key={spot.id} className="card p-6">
              <div className="flex items-start justify-between gap-4 mb-4">
                <div>
                  <h3 className="font-bold text-gray-900 text-lg">{spot.name_ar}</h3>
                  {spot.name_en && <p className="text-gray-400 text-sm">{spot.name_en}</p>}
                </div>
                <Badge variant="yellow">{isArabic ? "بانتظار المراجعة" : "Pending"}</Badge>
              </div>

              <p className="text-gray-600 text-sm mb-4 line-clamp-3">{spot.description_ar}</p>

              <div className="flex flex-wrap gap-3 text-xs text-gray-500 mb-4">
                <span>📍 {spot.latitude.toFixed(4)}, {spot.longitude.toFixed(4)}</span>
                <span>🏷 {spot.spot_type}</span>
                <span>⚡ {spot.access_difficulty}</span>
                {spot.ai_quality_score && (
                  <span>🤖 AI Score: {(spot.ai_quality_score * 100).toFixed(0)}%</span>
                )}
              </div>

              {spot.ai_quality_notes && (
                <div className="p-3 bg-blue-50 border border-blue-100 rounded-xl text-sm text-blue-700 mb-4">
                  <span className="font-medium">🤖 {isArabic ? "ملاحظات الذكاء الاصطناعي: " : "AI Notes: "}</span>
                  {spot.ai_quality_notes}
                </div>
              )}

              <div className="flex items-start gap-3">
                <Button
                  variant="primary"
                  size="sm"
                  loading={processing[spot.id]}
                  onClick={() => handleApproval(spot.id, true)}
                >
                  {isArabic ? "موافقة ✅" : "Approve ✅"}
                </Button>

                <div className="flex-1 flex gap-2">
                  <input
                    type="text"
                    placeholder={isArabic ? "سبب الرفض..." : "Rejection reason..."}
                    className="input-field text-sm flex-1"
                    value={rejectionReason[spot.id] || ""}
                    onChange={(e) => setRejectionReason((prev) => ({ ...prev, [spot.id]: e.target.value }))}
                  />
                  <Button
                    variant="danger"
                    size="sm"
                    loading={processing[spot.id]}
                    onClick={() => handleApproval(spot.id, false)}
                  >
                    {isArabic ? "رفض" : "Reject"}
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </PageWrapper>
  );
}
