import streamlit as st
import json

# قائمة لتخزين المخاطر
risks = []
risk_id = 1

# إضافة خطر جديد
def add_risk(name_risk, desk_risk, type_risk, grad_probability, grad_impact):
    global risk_id
    risk_level = grad_probability * grad_impact
    risk = {
        "risk_id": risk_id,
        "name_risk": name_risk,
        "desk_risk": desk_risk,
        "type_risk": type_risk,
        "grad_probability": grad_probability,
        "grad_impact": grad_impact,
        "risk_level": risk_level
    }
    risks.append(risk)
    risk_id += 1
    st.success(f"✅ تم إضافة الخطر بنجاح | مستوى الخطر: {risk_level}")

# عرض كل المخاطر
def display_risks():
    if len(risks) == 0:
        st.warning("⚠️ لا توجد مخاطر مسجلة.")
    else:
        st.write("📋 قائمة المخاطر:")
        for risk in risks:
            st.write(f"- رقم: {risk['risk_id']} | اسم: {risk['name_risk']} | نوع: {risk['type_risk']} | مستوى: {risk['risk_level']}")

# البحث عن خطر
def search_risk(search_value):
    found = False
    for risk in risks:
        if risk['name_risk'].lower() == search_value.lower() or risk['type_risk'].lower() == search_value.lower():
            st.success("✅ تم العثور على الخطر:")
            st.write(risk)
            found = True
    if not found:
        st.warning("⚠️ لا توجد مخاطر بهذا الاسم أو النوع.")

# تحديث الخطر
def update_risk(num_risk, name_risk, desk_risk, type_risk, grad_probability, grad_impact):
    found = False
    for risk in risks:
        if risk["risk_id"] == num_risk:
            risk["name_risk"] = name_risk
            risk["desk_risk"] = desk_risk
            risk["type_risk"] = type_risk
            risk["grad_probability"] = grad_probability
            risk["grad_impact"] = grad_impact
            risk["risk_level"] = grad_probability * grad_impact
            st.success("✅ تم تحديث بيانات الخطر بنجاح.")
            found = True
            break
    if not found:
        st.warning("⚠️ لم يتم العثور على هذا الخطر.")

# حذف خطر
def delete_risk(delete_id):
    found = False
    for risk in risks:
        if risk["risk_id"] == delete_id:
            risks.remove(risk)
            st.success("✅ تم حذف الخطر بنجاح.")
            found = True
            break
    if not found:
        st.warning("⚠️ الخطر غير موجود.")

# ملخص المخاطر
def risk_summary():
    if len(risks) == 0:
        st.warning("⚠️ لا توجد مخاطر لحساب الملخص.")
        return
    total = len(risks)
    avg_level = sum(r['risk_level'] for r in risks) / total
    high_risks = [r for r in risks if r['risk_level'] >= 15]
    st.write("📊 ملخص المخاطر:")
    st.write(f"إجمالي عدد المخاطر: {total}")
    st.write(f"متوسط مستوى المخاطر: {avg_level:.2f}")
    st.write(f"عدد المخاطر العالية: {len(high_risks)}")

# حفظ البيانات في ملف
def save_risks():
    with open("risks.json", "w", encoding="utf-8") as file:
        json.dump(risks, file, ensure_ascii=False, indent=2)
        st.success("💾 تم حفظ المخاطر في الملف بنجاح.")

# واجهة Streamlit
st.title("نظام إدارة المخاطر (Risk Management)")

menu = ["إضافة خطر", "عرض المخاطر", "البحث عن خطر", "تحديث خطر", "حذف خطر", "ملخص المخاطر", "حفظ البيانات"]
choice = st.sidebar.selectbox("اختر العملية", menu)

if choice == "إضافة خطر":
    st.subheader("إضافة خطر جديد")
    name_risk = st.text_input("اسم الخطر")
    desk_risk = st.text_area("وصف الخطر")
    type_risk = st.text_input("نوع الخطر")
    grad_probability = st.number_input("درجة الاحتمالية من 1 إلى 5", 1, 5)
    grad_impact = st.number_input("درجة التأثير من 1 إلى 5", 1, 5)
    if st.button("أضف الخطر"):
        add_risk(name_risk, desk_risk, type_risk, grad_probability, grad_impact)

elif choice == "عرض المخاطر":
    display_risks()

elif choice == "البحث عن خطر":
    search_value = st.text_input("ادخل اسم أو نوع الخطر للبحث")
    if st.button("بحث"):
        search_risk(search_value)

elif choice == "تحديث خطر":
    num_risk = st.number_input("رقم الخطر المراد تحديثه", 1, 1000)
    name_risk = st.text_input("اسم الخطر الجديد")
    desk_risk = st.text_area("وصف الخطر الجديد")
    type_risk = st.text_input("نوع الخطر الجديد")
    grad_probability = st.number_input("درجة الاحتمالية من 1 إلى 5", 1, 5)
    grad_impact = st.number_input("درجة التأثير من 1 إلى 5", 1, 5)
    if st.button("تحديث الخطر"):
        update_risk(num_risk, name_risk, desk_risk, type_risk, grad_probability, grad_impact)

elif choice == "حذف خطر":
    delete_id = st.number_input("رقم الخطر المراد حذفه", 1, 1000)
    if st.button("حذف الخطر"):
        delete_risk(delete_id)

elif choice == "ملخص المخاطر":
    risk_summary()

elif choice == "حفظ البيانات":
    if st.button("حفظ"):
        save_risks()
