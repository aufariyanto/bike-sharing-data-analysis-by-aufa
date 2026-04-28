# 3. CUACA
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Berdasarkan Cuaca")
    fig, ax = plt.subplots(figsize=(10, 6))
    # Logika penentuan warna: Highlight warna biru untuk nilai maksimum, sisanya abu-abu
    colors_weather = ["#72BCD4" if val == weather_rent_df['cnt'].max() else "#D3D3D3" for val in weather_rent_df['cnt']]
    sns.barplot(
        x='weathersit_label',
        y='cnt',
        data=weather_rent_df,
        hue='weathersit_label',
        palette=colors_weather, # Memasukkan list warna khusus
        legend=False,
        ax=ax
    )
    plt.xlabel('Kondisi Cuaca', fontsize=12, fontweight='bold')
    plt.ylabel('Rata-rata Jumlah Penyewaan Harian (Unit)', fontsize=12, fontweight='bold')
    st.pyplot(fig)

with col_b:
    st.subheader("Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(10, 6))
    # Logika penentuan warna: Highlight warna biru untuk nilai maksimum, sisanya abu-abu
    colors_season = ["#72BCD4" if val == season_rent_df['cnt'].max() else "#D3D3D3" for val in season_rent_df['cnt']]
    sns.barplot(
        x='season_label',
        y='cnt',
        data=season_rent_df,
        hue='season_label',
        palette=colors_season, # Memasukkan list warna khusus
        legend=False,
        ax=ax
    )
    plt.xlabel('Kondisi Musim', fontsize=12, fontweight='bold')
    plt.ylabel('Jumlah Penyewaan Harian (Unit)', fontsize=12, fontweight='bold')
    st.pyplot(fig)
    st.pyplot(fig)
