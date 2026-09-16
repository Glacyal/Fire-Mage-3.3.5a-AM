"""
Modulo Componente: 10 - Alerts
==============================
Gestisce gli avvisi testuali contestuali centrali (a y = 105):
- Alert - Hot Streak: Scritta a due righe in centro schermo quando Hot Streak è attivo
  (|cFFFF5500HOT STREAK!|r\\n|cFFFFFF00PYROBLAST READY!|r).
"""


def build_alerts_auras() -> list[dict]:
    """
    Costruisce e restituisce le aure del gruppo Alerts:
    - 10 - Alerts (Group)
    - Alert - Hot Streak (Text)
    """
    return [
        {
            "id": "10 - Alerts",
            "uid": "FMHUD_ALERTS_GRP",
            "parent": "Fire Mage 3.3.5a AM",
            "regionType": "group",
            "internalVersion": 52,
            "xOffset": 0,
            "yOffset": 105,
            "controlledChildren": [
                "Alert - Hot Streak"
            ],
        },
        {
            "id": "Alert - Hot Streak",
            "uid": "FMHUD_ALERT_HS",
            "parent": "10 - Alerts",
            "regionType": "text",
            "internalVersion": 52,
            "displayText": "|cFFFF5500HOT STREAK!|r\\n|cFFFFFF00PYROBLAST READY!|r",
            "fontSize": 20,
            "outline": "OUTLINE",
            "justify": "CENTER",
            "color": [1, 1, 1, 1],
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "xOffset": 0,
            "yOffset": 0,
            "triggers": {
                1: {
                    "trigger": {
                        "type": "aura2",
                        "unit": "player",
                        "auranames": ["Hot Streak"],
                        "useName": True,
                        "debuffType": "HELPFUL",
                        "matchesShowOn": "showOnActive",
                    },
                    "untrigger": {}
                },
                "activeTriggerMode": -10,
            },
        },
    ]
