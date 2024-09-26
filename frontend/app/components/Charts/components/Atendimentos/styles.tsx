import styled from "styled-components";

export const AtendimentosSection = styled.div`
  h1 {
    margin-bottom: 56px;
  }

  h2 {
    font-size: 56px;
    line-height: 40px;
    color: #632956;
  }

  h3 {
    font-size: 16px;
    color: #632956;
  }

  p {
    font-size: 12px;
    color: #585B5F;
  }
`;

export const AtendimentosContent = styled.div`
  display: grid;
  gap: 42px;
`;

export const FourGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: 32px;
`;

export const BigNumber = styled.div`
  display: flex;
  align-items: end;

  gap: 16px;

  margin-bottom: 10px;
`;

export const Number = styled.div`
  display: flex;
  align-items: end;

  gap: 8px;
`;
