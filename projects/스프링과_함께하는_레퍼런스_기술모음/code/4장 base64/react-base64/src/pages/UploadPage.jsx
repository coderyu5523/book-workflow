import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { imageApi } from "../api/imageApi";

export default function UploadPage() {
  // navigate 함수: 업로드 후 "/" 페이지로 이동하기 위해 사용
  const navigate = useNavigate();

  // file: 실제 사용자가 선택한 파일 객체(File 타입)
  // preview: 선택한 이미지를 화면에 보여주기 위한 Blob URL
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");

  /**
   * handleFileChange
   * - input type="file" 에서 파일이 선택되면 실행되는 함수
   * - e.target.files[0]는 사용자가 선택한 첫 번째 파일(File 객체)
   * - URL.createObjectURL: 브라우저가 제공하는 Blob(Binary Large Object, 브라우저 객체 타입)URL 생성 API로,
   *   실제 파일 내용을 서버에 보내지 않아도 화면에서 즉시 미리보기 가능
   */
  const handleFileChange = (e) => {
    const f = e.target.files[0];
    setFile(f);

    // 브라우저가 메모리에 임시 URL을 생성해 이미지 미리보기 가능
    // 이 URL은 실제 파일이 아니라 Blob을 가리키는 임시 경로
    setPreview(URL.createObjectURL(f));
  };

  /**
   * handleUpload
   * - 파일을 Base64로 변환해 서버에 업로드하는 함수
   * - FileReader는 브라우저 내장 API로 파일을 읽고 문자열·ArrayBuffer로 변환 가능
   */
  const handleUpload = async () => {
    // 파일이 없으면 중단
    if (!file) return alert("파일을 선택하세요.");

    // FileReader:
    // 브라우저에서 제공하는 비동기 파일 읽기 API
    // 파일 읽기는 즉시 끝나지 않고, readAsDataURL 실행 후 loadend 이벤트에서 결과 접근
    const reader = new FileReader();

    /**
     * reader.onloadend
     * - 파일 읽기가 끝났을 때 실행되는 콜백
     * - reader.result 값은 "data:image/png;base64,xxx" 형태의 전체 문자열
     *   → 앞부분의 "data:image/png;base64," 는 파일 형식 정보
     *   → 실제 Base64 데이터는 "," 뒤쪽만 추출해야 한다.
     */
    reader.onloadend = async () => {
      // "data:image/png;base64,AAAA..." 형식에서 base64 부분만 추출
      const base64 = reader.result.split(",")[1];

      try {
        // 서버 업로드 요청 (파일명, base64)
        await imageApi.upload(file.name, base64);

        alert("업로드 완료!");

        // 업로드 완료 후 페이지 이동
        navigate("/");
      } catch (err) {
        console.error(err);
        alert("업로드 실패!");
      }
    };

    /**
     * reader.readAsDataURL(file)
     * readAsDataURL:
     *   - 파일을 읽어서 base64로 인코딩한 문자열(Data URL)을 생성
     *   - 비동기적으로 처리되며, 완료되면 onloadend가 호출됨
     *   - 이미지 업로드 시 backend로 base64 문자열을 보내고 싶을 때 사용
     */
    reader.readAsDataURL(file);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2> 업로드 페이지</h2>

      {/* accept="image/*" 
          - 사용자에게 이미지 파일만 선택하도록 제한하는 input 속성
      */}
      <input type="file" accept="image/*" onChange={handleFileChange} />

      {/* 파일이 선택되면 preview URL로 미리보기 이미지를 렌더링 */}
      {preview && (
        <img style={{ width: 500, height: 500 }} src={preview} alt="preview" />
      )}

      <br />

      {/* 업로드 버튼 */}
      <button style={{ marginTop: 10, width: 200 }} onClick={handleUpload}>
        업로드
      </button>
    </div>
  );
}