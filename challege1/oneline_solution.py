df.insert(1,'diff',df['hour'] - df['hour'].shift(1).fillna(value=0))
