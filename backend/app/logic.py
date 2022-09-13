from . import errors, crud


def get_variant_list(query_params):
    data = crud.get_vcf_data()
    if query_params.ID:
        data = data.query(f'ID == "{query_params.ID}"')
    prev_page = query_params.page - 1
    cur_page = query_params.page
    result = []
    values = data.values
    if len(values) > prev_page*10:
        for i in range(prev_page*10, cur_page*10):
            if i > len(values) - 1:
                break
            result.append({
                "CHROM": values[i][0].strip(),
                "POS": values[i][1],
                "ID": values[i][2].strip(),
                "REF": values[i][3].strip(),
                "ALT": values[i][4].strip(),
            })
    if not result:
        raise errors.JsonException(
            message=errors.NO_VARIANTS_FOUND, code=404)
    return result


def create_variant(variant):
    data = crud.get_vcf_data()
    record = crud.create_record(variant)
    data = data.append(record, ignore_index=True)
    crud.save_data(data)


def edit_variant(ID, variant):
    data = crud.get_vcf_data()
    if not len(data.loc[data['ID'] == ID]):
        raise errors.JsonException(
            message=errors.NO_VARIANTS_FOUND, code=404)
    cols = ["CHROM", "POS", "ID", "REF", "ALT"]
    variant_dict = variant.dict()
    for i in range(5):
        data.loc[data['ID'] == ID, data.columns[i]] = variant_dict[cols[i]]
    crud.save_data(data)


def delete_variant(ID):
    data = crud.get_vcf_data()
    if not len(data.loc[data['ID'] == ID]):
        raise errors.JsonException(
            message=errors.NO_VARIANTS_FOUND, code=404)
    data.drop(list(data.loc[data['ID'] == ID].index), axis=0, inplace=True)
    crud.save_data(data)
